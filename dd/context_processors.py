from base.models import Service
from carts.models import Cart
from django.template.loader import render_to_string

def get_session_cart(request):
    cart_obj,created = Cart.objects.new_or_get(request)
    return {
        'cart': render_to_string('cart.html', {'cart': cart_obj}),
        'cart_count': len(cart_obj.items.all())
    }
    
def get_services(request):
    services = Service.objects.all()
    return {
        'services':services
    }