from django.conf import settings
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import Service, ContactRequest

import requests
import json
import sweetify

def contact(request):
    if request.method == 'POST':
        data = request.POST
        fname = data['first-name']
        lname = data['last-name']
        email = data['email']
        phone = data['phone']
        message = data['message']
        recaptcha = data['g-recaptcha-response']
        params = {'secret': str(settings.RECAPTCHA_SECRET_KEY), 'response': recaptcha}
        if recaptcha != '':
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=params)
            response = json.loads(r.content)
            if response['success'] == True:
                request_obj = ContactRequest()
                request_obj.first_name = fname
                request_obj.last_name = lname
                request_obj.email = email
                request_obj.phone = phone
                request_obj.message = message
                request_obj.save()
                request.session['alert_message'] = 'success'
                from_email = 'info@eliftcreations.com'
                notif_subject = "New Contact Us Request! | Dominique's Dishes"
                notif_content = render_to_string('contact-request-received.html', 
                {
                    'first_name': fname,
                    'last_name': lname,
                    'email': email,
                    'phone': phone,
                    'message': message,
                    'timestamp': request_obj.created
                })
                notif_plain_text = 'New Contact Request Received'
                send_mail(notif_subject, notif_plain_text, from_email, ['dominiquesdishes@gmail.com','carolyn@dominiquesdishes.com'], html_message=notif_content)
                sweetify.success(request, "Thanks! We've received your request", persistent='Ok')
            else:
                sweetify.error(request, 'Uh oh! Something went wrong. Please refresh and try again', persistent='Ok')
        else:
            sweetify.error(request, "Uh oh! We couldn't verify you're a human. Please refresh the page and try again", persistent='Ok')
        return redirect('/contact/')
    else:
        context = {
            'title': "Dominique's Dishes | Contact Us",
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
        }
        return render(request, 'contact.html', context)

def home(request):
    context = {
        'title': "Dominique's Dishes | Home"
    }
    return render(request, 'home.html', context)

def story(request):
    context = {
        'title': "Dominique's Dishes | Story"
    }
    return render(request, 'story.html', context)

def service_detail(request, slug):
    service_obj = Service.objects.get(slug=slug)
    context = {
        'title': "Dominique's Dishes | %s" %(service_obj.title),
        'service': service_obj,
    }
    return render(request, 'service-detail.html', context)