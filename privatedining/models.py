from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from dd.utils import unique_obj_id_generator, unique_slug_generator

ITEM_TYPE_CHOICES = (
    ('starter', 'Starter'),
    ('entree', 'Entree'),
    ('side', 'Side'),
    ('dessert', 'Dessert'),
    ('beverage', 'Beverage'),
)
FONT_STYLE_CHOICES = (
    ('normal', 'Normal'),
    ('italic', 'Italic'),
)

class Item(models.Model):
    type                = models.CharField(choices=ITEM_TYPE_CHOICES, max_length=64)
    title               = models.CharField(max_length=270)
    description         = models.TextField(blank=True)
    price               = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title
        
class Section(models.Model):
    title               = models.CharField(max_length=270)
    description         = models.TextField(blank=True)
    items               = models.ManyToManyField(Item, blank=True)
    
    def __str__(self):
        return self.title

class Font(models.Model):
    title               = models.CharField(max_length=80, blank=True, null=True)
    weight              = models.IntegerField(default=400)
    style               = models.CharField(max_length=25, default='normal')
    
    def __str__(self):
        return self.title
    
class Menu(models.Model):
    obj_id              = models.CharField(max_length=64, blank=True, null=True)
    title               = models.CharField(max_length=270)
    slug                = models.SlugField(null=True, blank=True, unique=True)
    description         = models.TextField(blank=True)
    sections            = models.ManyToManyField(Section, blank=True)
    available           = models.BooleanField(default=True)
    title_font          = models.ForeignKey(Font, blank=True, null=True, on_delete=models.SET_NULL)
    title_color         = models.CharField(max_length=80, blank=True, null=True)
    background_color    = models.CharField(max_length=80, blank=True, null=True)
    background_image    = models.ImageField(blank=True, null=True)
    thumbnail           = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
def menu_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.obj_id:
        instance.obj_id = unique_obj_id_generator(instance)

pre_save.connect(menu_pre_save_receiver, sender=Menu)