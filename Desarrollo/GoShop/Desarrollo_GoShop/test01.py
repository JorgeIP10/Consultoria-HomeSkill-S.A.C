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

    # def test_signup_view_with_invalid_post_request(self):
    #     # First, create a user with the same username as the one we're going to try to create in this test
    #     User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
    #     data = {
    #         'username': 'testuser',
    #         'password1': 'testpassword',
    #         'password2': 'testpassword',
    #         'email': 'testuser2@example.com', # This email should be different from the one used above
    #     }
    #     response = self.client.post(self.signup_url, data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'register.html')
    #     self.assertContains(response, 'El usuario ya existe.')
    #     self.assertFalse(User.objects.filter(email='testuser2@example.com').exists())
