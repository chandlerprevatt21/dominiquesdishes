from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from customers.models import Customer
from .models import Cart, LineItem
from menus.models import Item
from orders.models import Order, PickupDate, PickupTime

import human_readable
import json
import stripe

def drop_carts(request):
    Cart.objects.all().delete()
    return HttpResponse('success')
    
def menu_cart_add(request):
    if request.method == 'POST':
        cart_obj,created = Cart.objects.new_or_get(request)
        try:
            entree = Item.objects.get(pk=request.POST['entree'])
        except:
            response = [
                {'status': 'error',
                 'message': 'Uh oh! That entree is no longer available'
                }
            ]
        try:
            sides = json.loads(request.POST['sides'])
        except:
            sides = None
        special_request = request.POST['request']
        item_obj = LineItem()
        item_obj.entree = str(entree)
        side_total = 0
        if sides is not None:
            side_dict = []
            for x in sides:
                side_obj = Item.objects.get(pk=x)
                side_dict.append(side_obj.title)
                side_total += side_obj.price
            side_list = human_readable.listing(side_dict, ',', "AND")
            item_obj.sides = side_list
        item_obj.notes = special_request
        
        entree_total = entree.price
        item_total = entree_total + side_total
        item_obj.price = item_total
        item_obj.save()
        cart_obj.items.add(item_obj)
        cart_obj.save()
        
        response = [
            {'status': 'success',
             'cart': render_to_string('cart.html', {'cart': cart_obj}),
             'cartCounter': len(cart_obj.items.all())
            }
        ]
        return JsonResponse(response, safe=False)

def menu_cart_remove(request):
    if request.method == 'POST':
        cart_obj,created = Cart.objects.new_or_get(request)
        try:
            item_obj = cart_obj.items.get(pk=request.POST['pk'])
            cart_obj.items.remove(item_obj)
            cart_obj.save()
            response = [
                {'status': 'success',
                'cart': render_to_string('cart.html', {'cart': cart_obj}),
                'cartCounter': len(cart_obj.items.all())
                }
            ]
        except:
            response = [
                {'status': 'error',
                 'message': 'Uh oh! That item has already been removed from the cart'
                }
            ]
        
        return JsonResponse(response, safe=False)
  
def menu_cart_update_pickup(request):
    if request.method == 'POST':
        cart_obj,created = Cart.objects.new_or_get(request)
        print(request.POST)
        try:
            date = PickupDate.objects.get(pk=request.POST['date'])
            time = PickupTime.objects.get(pk=request.POST['time'])
            cart_obj.pickup_date = date.date
            cart_obj.pickup_time = time.time
            cart_obj.save()
            data = {
                'status': 'success'
            }
            return JsonResponse(data, safe=False)
        except:
            data = {
                'status': 'error',
                'message': 'Pickup time unavailable. Please select a valid date and time',
            }
            return JsonResponse(data, safe=False)
        
def checkout(request):
    cart_obj,created = Cart.objects.new_or_get(request)
    stripe.api_key = settings.STRIPE_API_KEY
    stripe_connect_acct = settings.STRIPE_CONNECT_ACCT
    cart_total = cart_obj.get_stripe_total
    app_fee = cart_obj.get_app_fee
    pickup_dates = PickupDate.objects.filter(date__gte=datetime.now() + timedelta(days=1))
    response = stripe.PaymentIntent.create(
        amount=cart_total,
        currency="usd",
        automatic_payment_methods={'enabled':True},
        application_fee_amount=app_fee,
        stripe_account=str(stripe_connect_acct)
    )
    cart_obj.stripe_token = response.id
    cart_obj.save()
    client_secret = response.client_secret
    context = {
        "client_secret": client_secret,
        "cart": cart_obj,
        "title": "Checkout | Dominique's Dishes",
        "pickup_dates": pickup_dates,
        "public_key": settings.STRIPE_PUB_KEY,
        "stripe_connect_acct": stripe_connect_acct,
        "checkout_return_url": settings.CHECKOUT_RETURN_URL,
    }
    return render(request, 'checkout.html', context)

def checkout_success(request):
    cart_obj,created = Cart.objects.new_or_get(request)
    stripe.api_key = settings.STRIPE_API_KEY
    stripe_connect_acct = settings.STRIPE_CONNECT_ACCT
    if cart_obj.stripe_token is not None:
        try:
            intent = stripe.PaymentIntent.retrieve(str(cart_obj.stripe_token),
            stripe_account=str(stripe_connect_acct))
            try:
                order_obj = Order.objects.get(obj_id = intent.metadata.order_id)
            except:
                status = intent.status
                if status == 'succeeded':
                    order_obj = Order()
                    order_obj.stripe_id = cart_obj.stripe_token
                    order_obj.status = 'new'
                    order_obj.subtotal = cart_obj.get_subtotal
                    order_obj.tax = cart_obj.get_tax
                    order_obj.total = int(intent.charges.data[0].amount) / 100
                    order_obj.pickup_date = cart_obj.pickup_date
                    order_obj.pickup_time = cart_obj.pickup_time
                    customer_obj, created = Customer.objects.get_or_create(
                        name = intent.charges.data[0].billing_details.name,
                        email = intent.charges.data[0].billing_details.email
                    )
                    if customer_obj is not None:
                        order_obj.customer = customer_obj
                    order_obj.save()
                    for x in cart_obj.items.all():
                        order_obj.items.add(x)
                    order_obj.cart = cart_obj
                    cart_obj.active = False
                    order_obj.save()
                    stripe.PaymentIntent.modify(
                        str(cart_obj.stripe_token),
                        metadata={"order_id": str(order_obj.obj_id)},
                        stripe_account=str(stripe_connect_acct)
                    )
                    cart_obj.save()
            payment_method = stripe.PaymentMethod.retrieve(intent.payment_method,stripe_account='acct_1MXADbFi9exjpGoH')
            from_email = 'info@eliftcreations.com'
            notif_subject = "New Order! | Dominique's Dishes"
            notif_content = render_to_string('order-received.html', 
            {
                'name': customer_obj.name,
                'email': customer_obj.email,
                'subtotal': order_obj.subtotal,
                'tax': order_obj.tax,
                'total': '%.2f' %(order_obj.total),
                'pickup_date': order_obj.pickup_date,
                'pickup_time': order_obj.pickup_time,
                'items': order_obj.items.all(),
                'payment_method': payment_method,
                'timestamp': order_obj.created,
            })
            notif_plain_text = 'New Order Received'
            notif_recipients = ['carolyn@dominiquesdishes.com','dominiquesdishes@gmail.com', 'chandler@eliftcreations.com']
            #notif_recipients = ['chandler@eliftcreations.com']
            send_mail(notif_subject, notif_plain_text, from_email, notif_recipients, html_message=notif_content)
            
            receipt_subject = "Dominique's Dishes | Order Confirmation: %s" %(order_obj.obj_id)
            receipt_content = render_to_string('receipt.html', 
            {
                'order': order_obj,
                'payment_method': payment_method,
                'timestamp': order_obj.created,
                'total': '%.2f' %(order_obj.total),
            })
            receipt_plain_text = "Order confirmation from Dominique's Dishes"
            send_mail(receipt_subject, receipt_plain_text, from_email, [str(order_obj.customer.email)], html_message=receipt_content)
            
            context = {
                'title': 'Payment Confirmation - Order #%s' %(order_obj.obj_id),
                'order': order_obj,
                'card': payment_method
            }
            return render(request, 'checkout-success.html', context)
        except:
            return render(request, 'checkout-error.html', context)
    else:
        return redirect('/menus/')
    
def get_times(request):
    if request.method == 'POST':
        obj_pk = request.POST.get('obj')
        date_obj = PickupDate.objects.get(pk=obj_pk)
        times = date_obj.pickup_times.all
        data = {
            'status': 'success',
            'times': render_to_string('pickup-times.html', {'times': times}),
        }
        return JsonResponse(data)