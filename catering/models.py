from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from address.models import AddressField
from customers.models import Customer
from menus.models import Font

from dd.utils import unique_obj_id_generator, unique_slug_generator

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
    obj_id              = models.CharField(max_length=64, blank=True, null=True)
    type                = models.CharField(max_length=64, blank=True, null=True, default="catering")
    title               = models.CharField(max_length=270)
    slug                = models.SlugField(null=True, blank=True, unique=True)
    description         = models.TextField(blank=True)
    sections            = models.ManyToManyField(Section, blank=True)
    available           = models.BooleanField(default=True)
    title_font          = models.ForeignKey(Font, related_name='catering_menu_font', blank=True, null=True, on_delete=models.SET_NULL)
    title_color         = models.CharField(max_length=80, blank=True, null=True)
    text_color          = models.CharField(max_length=80, null=True, blank=True, default='white')
    background_color    = models.CharField(max_length=80, blank=True, null=True)
    background_image    = models.ImageField(blank=True, null=True)
    thumbnail           = models.ImageField(blank=True, null=True)
    created             = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated             = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('catering:menu-detail', args=[str(self.slug)])
    
def menu_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.obj_id:
        instance.obj_id = unique_obj_id_generator(instance)

pre_save.connect(menu_pre_save_receiver, sender=Menu)

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