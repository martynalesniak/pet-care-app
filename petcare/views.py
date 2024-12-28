from django.shortcuts import render
from .models import Post, Pet

def pet_list(request):
    pets = Pet.objects.all()
    return render(request, 'petcare/pet_list.html', {'pets': pets})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'petcare/post_list.html', {'posts': posts})
# Create your views here.
