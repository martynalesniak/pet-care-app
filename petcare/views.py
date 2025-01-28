from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Pet, UserProfile
from .forms import RegisterForm, PostForm, PetForm

def index(request):
    posts = Post.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.is_active = False
            user.save()
            UserProfile.objects.create(user=user)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            verification_link = request.build_absolute_uri(
                f"/confirm-email/{uid}/{token}/"
            )
            subject = 'Confirm your email'
            message = render_to_string('emails/confirm_email.html', {
                'user': user,
                'verification_link': verification_link,
            })
            send_mail(
                subject,
                message,
                'noreply@example.com', 
                [user.email],
                fail_silently=False,
            )

            return HttpResponseRedirect(reverse('email_confirmation_sent'))
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def email_confirmation_sent(request):
    return render(request, 'emails/email_confirmation_sent.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('index') 
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been successfully activated!')
        return render(request, 'emails/email_activated.html')
    else:
        messages.error(request, 'The confirmation link is invalid or has expired.')
        return render(request, 'emails/email_invalid.html')
    
@login_required
def profile(request):
    user_pets = request.user.pets.all()  
    user_posts = Post.objects.filter(user=request.user)
    
    return render(request, 'profile.html', {
        'pets': user_pets,
        'posts': user_posts  
    })

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('profile')
    else:
        form = PetForm()
    return render(request, 'add_pet.html', {'form': form}) 

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    posts = pet.posts.filter(is_active=True).order_by('-created_at') 
    return render(request, 'pet_detail.html', {'pet': pet, 'posts': posts})

@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if pet.owner != request.user:
        return redirect('profile') 
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = PetForm(instance=pet) 

    return render(request, 'edit_pet.html', {'form': form, 'pet': pet})

@login_required
def add_post(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pet = pet  
            post.user = request.user 
            post.save()
            return redirect('profile')  
    else:
        form = PostForm()  
    return render(request, 'add_post.html', {'form': form, 'pet': pet})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id) 
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return redirect('profile') 
    if request.method == 'POST': 
        post.delete() 
        return redirect('profile')  

    return HttpResponse("Invalid request", status=400)

@login_required
def apply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    pet_owner = post.pet.owner


    subject = f"Application for {post.pet.name}'s Post"
    message = (
        f"Hello {pet_owner.username},\n\n"
        f"{request.user.username} is interested in your post about {post.pet.name}.\n\n"
        f"Start Date: {post.start_date}\n"
        f"End Date: {post.end_date}\n\n"
        f"Contact Details of the Applicant:\n"
        f"Name: {request.user.first_name} {request.user.last_name}\n"
        f"Email: {request.user.email}\n\n"
        "Best regards,\nPawPal Team"
    )
    
    recipient_list = [pet_owner.email]

    try:
        send_mail(subject, message, 'noreply@pawpal.com', recipient_list)
        messages.success(request, "Your application has been sent successfully.")
    except Exception as e:
        messages.error(request, "There was an error sending your application. Please try again later.")

    return redirect('pet_detail', pet_id=post.pet.id)
