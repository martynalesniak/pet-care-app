from django.contrib import admin
from .models import Post, Pet, User
# Register your models here.

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'owner', 'energy_level')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pet', 'start_date', 'end_date', 'is_active', 'user')