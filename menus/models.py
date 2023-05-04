from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from dd.utils import unique_obj_id_generator, unique_slug_generator

ITEM_TYPE_CHOICES = (
    ('entree', 'Entree'),
    ('side', 'Side'),
    ('dessert', 'Dessert'),
    ('beverage', 'Beverage'),
)
FONT_STYLE_CHOICES = (
    ('normal', 'Normal'),
    ('italic', 'Italic'),
)
ORDER_OPTION_CHOICES = (
    ('meal', 'meal'),
    ('individual', 'individual'),
)


class Item(models.Model):
    type                = models.CharField(choices=ITEM_TYPE_CHOICES, max_length=64)
    title               = models.CharField(max_length=270)
    description         = models.TextField(blank=True)
    price               = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    order_options       = models.CharField(choices=ORDER_OPTION_CHOICES, max_length=64, default='individual')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['price', 'title']
        
class Section(models.Model):
    type                = models.CharField(choices=ITEM_TYPE_CHOICES, max_length=64, default='entree')
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
    type                = models.CharField(max_length=64, blank=True, null=True, default="regular")
    title               = models.CharField(max_length=270)
    slug                = models.SlugField(null=True, blank=True, unique=True)
    description         = models.TextField(blank=True)
    sections            = models.ManyToManyField(Section, blank=True)
    available           = models.BooleanField(default=True)
    title_font          = models.ForeignKey(Font, blank=True, null=True, on_delete=models.SET_NULL)
    title_color         = models.CharField(max_length=80, blank=True, null=True)
    text_color          = models.CharField(max_length=80, null=True, blank=True, default='white')
    background_color    = models.CharField(max_length=80, blank=True, null=True)
    background_image    = models.ImageField(blank=True, null=True)
    thumbnail           = models.ImageField(blank=True, null=True)
    max_sides           = models.IntegerField(default=0)
    position            = models.IntegerField(null=True, blank=True)
    created             = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated             = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('menus:detail', args=[str(self.slug)])
    
    class Meta:
        ordering = ['position']
    
def menu_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.obj_id:
        instance.obj_id = unique_obj_id_generator(instance)

pre_save.connect(menu_pre_save_receiver, sender=Menu)