from django.urls import path
from .views import home, quote, menu, detail

urlpatterns = [
    path('', home, name="home"),
    path('menu/', menu),
    path('request/', quote, name="request"),
    path('seasonal-menu/<slug>/', detail, name="menu-detail"),
]
