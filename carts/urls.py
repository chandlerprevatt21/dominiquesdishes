from django.urls import path
from .views import menu_cart_add, menu_cart_remove, menu_cart_update_pickup, checkout, checkout_success, get_times

urlpatterns = [
    path('add-menu-item/', menu_cart_add),
    path('remove-menu-item/', menu_cart_remove),
    path('update-pickup/', menu_cart_update_pickup),
    path('checkout/', checkout, name="checkout"),
    path('checkout-success/', checkout_success, name="success"),
    path('get-times/', get_times)
]
