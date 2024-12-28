from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .choices import Characteristic, EnergyLevel



class Pet(models.Model):
    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=40)
    color = models.CharField(max_length=20)
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    sex = models.CharField(max_length=6)
    description = models.TextField()
    characteristics = models.CharField(
        max_length=100,
        choices=Characteristic.choices,
        blank=True,
        null=True,
    )
    energy_level = models.IntegerField(choices=EnergyLevel.choices, default=EnergyLevel.MEDIUM)
    is_vaccinated = models.BooleanField(default=False)
    image = models.ImageField(upload_to='pets_images/', null=True, blank=True)
    location = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')

class Post(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='posts')
    start_date = models.DateField()
    end_date = models.DateField()
    care_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Whether the post is still active or expired
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)