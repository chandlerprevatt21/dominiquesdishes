from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from accounts.models import User
from customers.models import Customer
from dd.utils import unique_obj_id_generator

from decimal import *

class LineItem(models.Model):
    item_id             = models.CharField(max_length=64, blank=True, null=True)
    entree              = models.CharField(max_length=270, blank=True, null=True)
    sides               = models.CharField(max_length=270, blank=True, null=True)
    beverage            = models.CharField(max_length=270, blank=True, null=True)
    notes               = models.TextField(blank=True, null=True)
    price               = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return str(self.entree)

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id, active=True)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)
    
class Cart(models.Model):
    user                = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer            = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    obj_id              = models.CharField(max_length=64, unique=True, blank=True)
    active              = models.BooleanField(default=True)
    items               = models.ManyToManyField(LineItem, blank=True)
    pickup_date         = models.DateField(null=True, blank=True)
    pickup_time         = models.TimeField(null=True, blank=True)
    stripe_token        = models.CharField(max_length=380, blank=True, null=True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    
    objects             = CartManager()
    
    def __str__(self):
        return str(self.obj_id)
    
    def get_success_url(self):
        return reverse("payment-success", kwargs={"cart_pk":self.pk})
    
    @property
    def get_subtotal(self):
        objs = self.items.all()
        prices = []
        for x in objs:
            prices.append(int(x.price))
        total = sum(prices)
        formatted_total = "{}.00".format(total)
        return formatted_total
    
    @property
    def get_tax(self):
        objs = self.items.all()
        prices = []
        for x in objs:
            prices.append(int(x.price))
        total = sum(prices)
        tax = int(total * 0.08)
        formatted_total = "{}.00".format(tax)
        return formatted_total
    
    @property
    def get_total(self):
        objs = self.items.all()
        prices = []
        for x in objs:
            prices.append(int(x.price))
        total = sum(prices)
        tax = int(total * 0.08)
        formatted_total = "{}.00".format(total + tax)
        return formatted_total
    
    @property
    def get_stripe_total(self):
        objs = self.items.all()
        prices = []
        for x in objs:
            prices.append(int(x.price))
        total = sum(prices)
        tax = int(total * 0.08)
        formatted_total = "{}00".format(total + tax)
        return formatted_total
    
    @property
    def get_app_fee(self):
        total = self.get_stripe_total
        dec = Decimal(int(total)/100)
        app_fee = int(dec * Decimal(0.021) * Decimal(100))
        return app_fee

def cart_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.obj_id:
        instance.obj_id = unique_obj_id_generator(instance)

pre_save.connect(cart_pre_save_receiver, sender=Cart)