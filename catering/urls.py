from django.urls import path
from .views import home, quote, menu

urlpatterns = [
    path('', home, name="home"),
    path('menu/', menu),
    path('request/', quote, name="request"),
]
