from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.signout_url = reverse('signout')
        self.shop_url = reverse('shop')
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')

    def test_signup_view(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        
        response = self.client.post(self.signup_url, {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword', 'email': 'newuser@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.shop_url)
        
        response = self.client.post(self.signup_url, {'username': 'testuser', 'password1': 'newpassword', 'password2': 'newpassword', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'El usuario ya existe.')
        
    def test_signin_view(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        
        response = self.client.post(self.signin_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.shop_url)
        
        response = self.client.post(self.signin_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Usuario y/o contraseña incorrecto(s).')
        
    def test_signout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.shop_url)
        self.assertFalse('_auth_user_id' in self.client.session)
        
    def test_shop_view(self):
        response = self.client.get(self.shop_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
