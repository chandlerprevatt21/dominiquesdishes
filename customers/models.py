from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

class Customer(models.Model):
    customer_id             = models.CharField(max_length=240, blank=True, null=True)
    first_name              = models.CharField(max_length=120, blank=True, null=True)
    last_name               = models.CharField(max_length=120, blank=True, null=True)
    name                    = models.CharField(max_length=120, blank=True, null=True)
    email                   = models.EmailField(blank=True, null=True)
    phone                   = PhoneNumberField(blank=True)
    
    def __str__(self):
        try:
            return str(self.name)
        except:
            return 'Anonymous Shopper'