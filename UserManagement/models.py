import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.



class Role(models.Model):
    
    name = models.CharField(max_length=255)
    name_code = models.CharField(max_length=255)
    desc_role     = models.TextField()
    created_at   =  models.DateTimeField(default=timezone.now)
    updated_at   =  models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
    


class UserProfile(models.Model):

    TITLE_CHOICES = [
        ("Mr", "Mr"),
        ("Mme", "Mme"),
        ("Mlle", "Mlle"),
        ("Entreprise", "Entreprise"),
    ]
   
    user                = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    firstName           = models.CharField(max_length=255 , blank=True)
    lastName            = models.CharField(max_length=255, blank=True)
    fullName            = models.CharField(max_length=255)
    email               = models.EmailField(max_length=255 , null=True)
    phone               = models.CharField(max_length=255, null=True)
    profilImage         = models.ImageField(upload_to="image/users/profil")
    active              =  models.BooleanField(default=True)
    role                =  models.ForeignKey(Role , on_delete=models.SET_NULL, null=True)
    status              = models.CharField(max_length=255)
    quartier            = models.CharField(max_length=255, null=True)
    ville               = models.CharField(max_length=255, null=True)
    title               = models.CharField(max_length=255 , choices=TITLE_CHOICES , default='Mr')
    created_at          =  models.DateTimeField(default=timezone.now)
    updated_at          =  models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
    


    def save(self, *args, **kwargs):
        # Set fullName based on firstName and lastName before saving
        self.fullName = f"{self.firstName} {self.lastName}".strip()
        super(UserProfile, self).save(*args, **kwargs)



class Agency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    manager = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
    
