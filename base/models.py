from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from ckeditor.fields import RichTextField
from dd.utils import unique_slug_generator

class Service(models.Model):
    title               = models.CharField(max_length=270, unique=True)
    slug                = models.SlugField(blank=True, null=True)
    description         = RichTextField(blank=True, null=True)
    page_content        = RichTextField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('service-detail', args=[str(self.slug)])
    
    class Meta:
        ordering = ['title']

def service_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(service_pre_save_receiver, sender=Service)

class ContactRequest(models.Model):
    first_name          = models.CharField(max_length=270)
    last_name           = models.CharField(max_length=270)
    email               = models.EmailField()
    phone               = models.CharField(max_length=270, blank=True)
    message             = models.TextField()
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return 'Contact Request from %s %s' %(self.first_name, self.last_name)
    