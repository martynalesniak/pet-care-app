from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Pet

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number') 
            )
        
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['start_date', 'end_date', 'care_description', 'is_active']
        widgets = {
            'start_date': forms.SelectDateWidget,
            'end_date': forms.SelectDateWidget,
        }


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 'age', 'breed', 'height', 'weight', 'sex',
            'description', 'characteristics', 'energy_level', 
            'is_vaccinated', 'image', 'location'
        ]
        widgets = {
            'characteristics': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("You must upload an image.")
        return image