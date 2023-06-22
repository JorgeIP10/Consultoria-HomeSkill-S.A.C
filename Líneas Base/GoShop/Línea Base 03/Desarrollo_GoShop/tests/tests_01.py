from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class SignupViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.signout_url = reverse('logout')

    def test_signup_view_with_get_request(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_signup_view_with_valid_post_request(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shop'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_signin_get(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_signin_post(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shop'))
        self.assertEqual(str(response.wsgi_request.user), str(user))
    
    def test_signout_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('shop'))
        self.assertTrue(response.wsgi_request.user.is_anonymous)