from django.shortcuts import render, redirect
from .models import Post, Pet
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Zapisz użytkownika
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Przekierowanie do strony logowania po rejestracji
    else:
        form = RegisterForm()  # Używamy RegisterForm, a nie UserCreationForm
    
    return render(request, 'petcare/register.html', {'form': form})
