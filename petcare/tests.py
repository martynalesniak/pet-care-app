from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Pet, Characteristic, Post
from django.core.mail import send_mail
from django.core.files.temp import NamedTemporaryFile
from PIL import Image

class PublicViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'first_name': 'John',  
            'last_name': 'Doe',  
            'email': 'testuser@example.com',
            'password1': 'TestPassword123!',  
            'password2': 'TestPassword123!', 
            'phone_number': '1234567890',   
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user_profile = UserProfile.objects.get(user__username='testuser')


class AuthenticatedViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.characteristic1 = Characteristic.objects.create(name='Friendly')
        self.characteristic2 = Characteristic.objects.create(name='Playful')

    def create_temp_image(self):
        img = Image.new('RGB', (100, 100), color='blue')
        temp_file = NamedTemporaryFile(delete=False)
        img.save(temp_file, format='JPEG')
        temp_file.seek(0)
        return temp_file
    
    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_add_pet_view(self):
        temp_image = self.create_temp_image()
        with open(temp_image.name, 'rb') as img_file:
            image_file = SimpleUploadedFile(
                name='test_image.jpg',
                content=img_file.read(),
                content_type='image/jpeg'
            )
        
        response = self.client.get(reverse('add_pet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_pet.html')

        response = self.client.post(reverse('add_pet'), {
            'name': 'Fluffy',
            'age': 3,
            'breed': 'Labrador',
            'height': 50,
            'weight': 25,
            'sex': 'M',
            'description': 'A friendly dog',
            'characteristics': [self.characteristic1.id, self.characteristic2.id],
            'energy_level': 5,
            'is_vaccinated': True,
            'image': image_file,
            'location': 'New York',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pet.objects.filter(name='Fluffy').exists())

   
    def test_edit_pet_view(self):
        temp_image = self.create_temp_image()
        pet = Pet.objects.create(
            name='Fluffy',
            age=3,
            breed='Labrador',
            height=50,
            weight=25,
            sex='M',
            description='A friendly dog',
            energy_level=5,
            owner=self.user,
            is_vaccinated=True,
            location='New York',
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=open(temp_image.name, 'rb').read(),
                content_type='image/jpeg'
            )
        )
        pet.characteristics.set([self.characteristic1, self.characteristic2])
        pet.save()
        response = self.client.get(reverse('edit_pet', args=[pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_pet.html')

        response = self.client.post(reverse('edit_pet', args=[pet.id]), {
            'name': 'Fluffy Updated',  
            'age': 4,  
            'breed': 'Golden Retriever',  
            'height': 55, 
            'weight': 30,  
            'sex': 'F',  
            'description': 'A friendly and playful dog',  
            'characteristics': [self.characteristic1.id, self.characteristic2.id],
            'energy_level': 3,  
            'is_vaccinated': False,  
            'image': SimpleUploadedFile(
                name='test_image_updated.jpg',
                content=open(temp_image.name, 'rb').read(),
                content_type='image/jpeg'
            ),
            'location': 'Los Angeles',  
        })
        self.assertEqual(response.status_code, 302)
        pet.refresh_from_db()

        self.assertEqual(pet.name, 'Fluffy Updated')
        self.assertEqual(pet.age, 4)
        self.assertEqual(pet.breed, 'Golden Retriever')
        self.assertEqual(pet.sex, 'F')
        self.assertEqual(pet.height, 55)
        self.assertEqual(pet.weight, 30)
        self.assertEqual(pet.description, 'A friendly and playful dog')
        self.assertEqual(pet.energy_level, 3)
        self.assertFalse(pet.is_vaccinated)
        self.assertEqual(pet.location, 'Los Angeles')


class PostViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.characteristic1 = Characteristic.objects.create(name="Friendly")
        self.characteristic2 = Characteristic.objects.create(name="Playful")
        
        temp_image = self.create_temp_image()
        self.pet = Pet.objects.create(
            name='Fluffy',
            age=3,
            breed='Labrador',
            height=50,
            weight=25,
            sex='M',
            description='A friendly dog',
            energy_level=5,
            owner=self.user,
            is_vaccinated=True,
            location='New York',
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=open(temp_image.name, 'rb').read(),
                content_type='image/jpeg'
            )
        )
        self.pet.characteristics.set([self.characteristic1, self.characteristic2])
        self.pet.save()

        self.client.login(username='testuser', password='testpassword')

    def create_temp_image(self):
        img = Image.new('RGB', (100, 100), color='blue')
        temp_file = NamedTemporaryFile(delete=False)
        img.save(temp_file, format='JPEG')
        temp_file.seek(0)
        return temp_file
    
    def test_add_post_view(self):
        response = self.client.get(reverse('add_post', args=[self.pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_post.html')


        response = self.client.post(reverse('add_post', args=[self.pet.id]), {
            'care_description': 'Need someone to walk the dog daily',
            'start_date': '2025-02-01',
            'end_date': '2025-02-15',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(care_description='Need someone to walk the dog daily').exists())

    def test_apply_to_post_view(self):
        post = Post.objects.create(
            pet=self.pet,
            user=self.user,
            care_description='Need someone to feed the dog',
            start_date='2025-02-01',
            end_date='2025-02-15',
            is_active=True
        )
        response = self.client.post(reverse('apply_to_post', args=[post.id]))
        self.assertEqual(response.status_code, 302)



