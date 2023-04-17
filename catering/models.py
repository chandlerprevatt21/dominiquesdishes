from django.db import models

from address.models import AddressField
from customers.models import Customer

ITEM_TYPE_CHOICES = (
    ('entree', 'Entree'),
    ('side', 'Side'),
    ('beverage', 'Beverage'),
)

class Variation(models.Model):
    title               = models.CharField(max_length=270)
    description         = models.TextField(blank=True)
    size                = models.CharField(max_length=270)
    price               = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['size', 'price']
    
class Item(models.Model):
    title               = models.CharField(max_length=270)
    description         = models.TextField(blank=True, null=True)
    quarter_pan         = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    half_pan            = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    full_pan            = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    variations          = models.ManyToManyField(Variation, blank=True)
    vegan               = models.BooleanField(default=False)
    vegetarian          = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
        
class Section(models.Model):
    title               = models.CharField(max_length=270)
    description         = models.TextField(blank=True)
    items               = models.ManyToManyField(Item, blank=True)
    
    def __str__(self):
        return self.title
    
class Menu(models.Model):
    title               = models.CharField(max_length=270)
    description         = models.TextField(blank=True)
    sections            = models.ManyToManyField(Section, blank=True)

    def __str__(self):
        return self.title

class LineItem(models.Model):
    item_id             = models.CharField(max_length=64, blank=True, null=True)
    entree              = models.CharField(max_length=270, blank=True, null=True)
    sides               = models.CharField(max_length=270, blank=True, null=True)
    beverage            = models.CharField(max_length=270, blank=True, null=True)
    notes               = models.TextField(blank=True, null=True)
    price               = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.item_id
    
class Inquiry(models.Model):
    customer                = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    party_size              = models.IntegerField(default=4)
    event_date              = models.DateField(blank=True, null=True)
    event_time              = models.TimeField(blank=True, null=True) 
    event_location          = models.TextField(blank=True, null=True)
    services_needed         = models.TextField(blank=True, null=True)
    equipment_needed        = models.TextField(blank=True, null=True)
    special_instructions    = models.TextField(blank=True, null=True)
    allergies               = models.TextField(blank=True, null=True)
    onsite_cooking          = models.BooleanField(default=False)
    menu_items              = models.TextField(blank=True, null=True)
    created                 = models.DateTimeField(auto_now_add=True)
    updated                 = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return 'Catering Inquiry'
    
    class Meta:
        verbose_name = 'inquiry'
        verbose_name_plural = 'inquiries'