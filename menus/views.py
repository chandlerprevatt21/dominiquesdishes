from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from carts.models import Cart
from catering.models import Menu as CateringMenu
from .models import Menu, Item


def home(request):
    menus = Menu.objects.filter(available=True)
    archived = Menu.objects.filter(available=False)
    catering_menus = CateringMenu.objects.filter(available=True).exclude(slug="catering-menu")
    context = {
        'menus': menus,
        'archived': archived,
        'catering_menus': catering_menus,
        'title': "Dominique's Dishes | Menus",
    }
    return render(request, 'menu_home.html', context)

def detail(request, slug):
    try:
        obj = Menu.objects.get(slug=slug)
        cart_obj,created = Cart.objects.new_or_get(request)
        context = {
            'menu': obj,
            "title": "Dominique's Dishes | %s" %(obj.title),
            'cart': render_to_string('cart.html', {'cart': cart_obj}),
        }
        return render(request, 'menu_detail.html', context)
    except:
        raise Http404()
    
def item_form(request):
    if request.method == 'POST':
        item_pk = request.POST['itemID']
        menu_pk = request.POST['menu']
        try:
            menu_obj = Menu.objects.get(pk=menu_pk)
            item_obj = Item.objects.get(pk=item_pk)
            
            if item_obj.order_options == 'meal':
                
                side_sections = menu_obj.sections.filter(type='side')
                sides = []
                for section in side_sections:
                    for item in section.items.all():
                        sides.append(item)
            else:
                sides = []
            response = [
                {
                    'status': 'success',
                    'form': render_to_string('order_swal.html', {'item':item_obj,'sides':sides,'side_limit':menu_obj.max_sides}),
                }
            ]
        except:
            response = [
                {
                'status': 'error',
                'message': 'Uh oh! The item you selected is no longer available. Please choose another delicious option from one of our active menus!'
                }
            ]
        
        return JsonResponse(response, safe=False)
        