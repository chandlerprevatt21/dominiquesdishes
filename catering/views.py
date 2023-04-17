from django.conf import settings
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Menu, Inquiry
from customers.models import Customer
from django.core.mail import send_mail

import requests
import json
import sweetify

def home(request):
    context = {
        'title': "Catering | Dominique's Dishes",
    }
    return render(request, 'catering-home.html', context)

def quote(request):
    if request.method == 'POST':
        data = request.POST
        fname = data['first-name']
        lname = data['last-name']
        email = data['email']
        phone = data['phone']
        party_size = data['party-size']
        event_date = data['event-date']
        event_time = data['event-time']
        event_location = data['event-location']
        services_needed = data['services-needed']
        equipment_needed = data['equipment-needed']
        special_instructions = data['special-instructions']
        allergies = data['allergies']
        onsite_cooking = data['onsite-cooking']
        menu_items = data['menu-items']
        recaptcha = data['g-recaptcha-response']
        params = {'secret': str(settings.RECAPTCHA_SECRET_KEY), 'response': recaptcha}
        if recaptcha != '':
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=params)
            response = json.loads(r.content)
            if response['success'] == True:
                customer_obj, created = Customer.objects.get_or_create(name='%s %s' %(fname, lname))
                customer_obj.email = email
                customer_obj.save()
                request_obj = Inquiry()
                request_obj.customer = customer_obj
                request_obj.party_size = party_size
                request_obj.event_date = event_date
                request_obj.event_time = event_time
                request_obj.event_location = event_location
                request_obj.services_needed = services_needed
                request_obj.equipment_needed = equipment_needed
                request_obj.special_instructions = special_instructions
                request_obj.allergies = allergies
                request_obj.menu_items = menu_items
                if onsite_cooking == 'Yes':
                    request_obj.onsite_cooking = True
                else:
                    request_obj.onsite_cooking = False
                request_obj.save()
                from_email = 'info@eliftcreations.com'
                notif_subject = "New Catering Request! | Dominique's Dishes"
                notif_content = render_to_string('catering-request-received.html', 
                {
                    'first_name': fname,
                    'last_name': lname,
                    'email': email,
                    'phone': phone,
                    'party_size': party_size,
                    'event_date': event_date,
                    'event_time': event_time,
                    'event_location': event_location,
                    'services_needed': services_needed,
                    'equipment_needed': equipment_needed,
                    'special_instructions': special_instructions,
                    'menu_items': menu_items,
                    'allergies': allergies,
                    'timestamp': request_obj.created,
                })
                notif_plain_text = 'New Catering Request Received'
                send_mail(notif_subject, notif_plain_text, from_email, ['carolyn@dominiquesdishes.com','dominiquesdishes@gmail.com'], html_message=notif_content)
                sweetify.success(request, "Thanks! We've received your request and we'll be in touch shortly", persistent='Ok')
            else:
                sweetify.error(request, 'Uh oh! Something went wrong. Please refresh and try again', persistent='Ok')
        else:
            sweetify.error(request, "Uh oh! We couldn't verify you're a human. Please refresh the page and try again", persistent='Ok')
        return redirect('/catering/')
    else:
        context = {
            'title': "Catering Request | Dominique's Dishes",
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
        }
        return render(request, 'catering-quote.html', context)
    
def menu(request):
    menu_obj = Menu.objects.get(title='Catering Menu')
    context = {
        'title': "Catering Menu | Dominique's Dishes",
        'menu': menu_obj,
    }
    return render(request, 'catering-menu.html', context)