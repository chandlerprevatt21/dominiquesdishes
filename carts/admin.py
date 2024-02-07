from django.contrib import admin
from .models import Cart, LineItem

class CartAdmin(admin.ModelAdmin):
    list_per_page = 500
    
admin.site.register(Cart, CartAdmin)
admin.site.register(LineItem)
