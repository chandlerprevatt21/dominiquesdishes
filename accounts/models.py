from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

import random
import os

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "accounts/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError('An email address is required')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, password, email):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        
        return user

    def create_superuser(self, password, email):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True, null=True, blank=True, max_length=120)
    first_name = models.CharField(max_length=225, blank=True, null=True, unique=False)
    last_name = models.CharField(max_length=225, blank=True, null=True, unique=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=upload_image_path, blank=True, null=True)

    objects = UserManager()
    
    def __str__(self):
        return str(self.email)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def get_full_name(self):
        return '%s %s' %(self.first_name, self.last_name)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class GuestEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email