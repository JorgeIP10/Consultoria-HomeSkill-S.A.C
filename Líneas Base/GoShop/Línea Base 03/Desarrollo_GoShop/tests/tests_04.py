from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from UserProfile.views_profile import user_profile, user_config,confirm_user_config
from Ventas_Retail.models import Product,ProductCategory


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='testpass')
        self.client = Client()
        self.category = ProductCategory.objects.create(name='Test Category')
        self.product = Product.objects.create(
            id=1, name='TestProduct', price=100.0, category_id=self.category)

    def test_user_profile(self):
        request = self.factory.get(reverse('profile'))
        request.user = self.user
        response = user_profile(request)
        self.assertEqual(response.status_code, 200)

    def test_user_config(self):
        request = self.factory.get(reverse('config'))
        request.user = self.user
        response = user_config(request)
        self.assertEqual(response.status_code, 200)

    def test_confirm_user_config(self):
        request = self.factory.get(reverse('confirm_user_config', kwargs={'previous_view': 'profile', 'previous_name': 'name', 'mode': 'mode'}))
        request.user = self.user
        response = confirm_user_config(request, 'profile', 'name', 'mode')
        self.assertEqual(response.status_code, 200)