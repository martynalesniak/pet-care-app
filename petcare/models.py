from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .choices import Characteristic, EnergyLevel


class Characteristic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
class Pet(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=40)
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        blank=False,
        )
    description = models.TextField()
    characteristics = models.ManyToManyField(Characteristic, blank=True)
    energy_level = models.IntegerField(choices=EnergyLevel.choices, default=EnergyLevel.MEDIUM)
    is_vaccinated = models.BooleanField(default=False)
    image = models.ImageField(upload_to='pets_images/')
    location = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')
    def __str__(self):
        return self.name

class Post(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='posts')
    start_date = models.DateField()
    end_date = models.DateField()
    care_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)