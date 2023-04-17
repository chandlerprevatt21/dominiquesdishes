from django.db import models
from django.db.models.signals import pre_save

from carts.models import LineItem, Cart
from customers.models import Customer
from dd.utils import unique_obj_id_generator

ORDER_STATUS_CHOICES = (
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('ready', 'Ready'),
    ('picked_up', 'Picked Up'),
    ('delivered', 'Delivered'),
    ('complete', 'Complete'),
    ('refunded', 'Refunded'),
)

class PickupTime(models.Model):
    obj_id              = models.CharField(max_length=72, unique=True, blank=True)
    time                = models.TimeField()
    
    def __str__(self):
        return str(self.time)
    
    class Meta:
        ordering = ['time']
    
class PickupDate(models.Model):
    obj_id              = models.CharField(max_length=72, unique=True, blank=True)
    date                = models.DateField()
    pickup_times        = models.ManyToManyField(PickupTime, blank=True)
    
    def __str__(self):
        return str(self.date)
    
class Order(models.Model):
    obj_id              = models.CharField(max_length=72, unique=True, blank=True)
    stripe_id           = models.CharField(max_length=380, blank=True, null=True)
    customer            = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    status              = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=64, blank=True)
    items               = models.ManyToManyField(LineItem, blank=True)
    subtotal            = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default = 0.00)
    tax                 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default = 0.00)
    total               = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default = 0.00)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    cart                = models.ForeignKey(Cart, blank=True, null=True, on_delete=models.SET_NULL)
    pickup_date         = models.DateField(blank=True, null=True)
    pickup_time         = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return self.obj_id

def order_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.obj_id:
        instance.obj_id = unique_obj_id_generator(instance)

pre_save.connect(order_pre_save_receiver, sender=Order)
pre_save.connect(order_pre_save_receiver, sender=PickupDate)
pre_save.connect(order_pre_save_receiver, sender=PickupTime)