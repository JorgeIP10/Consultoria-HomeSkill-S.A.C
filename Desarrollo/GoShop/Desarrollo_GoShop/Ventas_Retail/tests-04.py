from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile
from django.urls import reverse


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        UserProfile.objects.get_or_create(user=self.user, username='testuser', email='testuser@example.com')

    def test_user_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('profile'))  
        self.assertEqual(response.status_code, 200)

    def test_user_config_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('config'))
        self.assertEqual(response.status_code, 200)


# class UsernameChangeViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
#         self.user.userprofile.username = 'testuser'
#         self.user.userprofile.password = '12345'
#         self.user.userprofile.email = 'testuser@example.com'
#         self.user.userprofile.save()

#     def test_change_username(self):
#         self.client.login(username='testuser', password='12345')
#         response = self.client.post(reverse('config'), data={'username': 'newusername'})
#         self.assertEqual(response.status_code, 200)
#         updated_user = User.objects.get(id=self.user.id)
#         self.assertEqual(updated_user.username, 'newusername')


class PasswordChangeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        UserProfile.objects.get_or_create(user=self.user, username='testuser', email='testuser@example.com')


    def test_change_password(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('config') + "/change/password", {'new-password': 'newpassword123'})
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=self.user.id)
        self.assertTrue(updated_user.check_password('newpassword123'))
