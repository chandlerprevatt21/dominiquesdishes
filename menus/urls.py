from django.urls import path
from .views import home, detail, item_form

urlpatterns = [
    path('', home, name="home"),
    path('item-form/', item_form),
    path('<slug>/', detail, name="detail"),
]
