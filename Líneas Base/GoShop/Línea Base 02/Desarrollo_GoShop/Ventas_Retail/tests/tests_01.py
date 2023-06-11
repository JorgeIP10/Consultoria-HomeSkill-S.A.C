from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class SignupViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

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