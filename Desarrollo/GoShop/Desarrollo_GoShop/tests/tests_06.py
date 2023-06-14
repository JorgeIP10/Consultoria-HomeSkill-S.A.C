from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from UserProfile.views_profile import shopping_history
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
    
    def test_shopping_history(self):
        #Se establece un estado de carrito de compras:
        session = self.client.session
        session['cart'] = {'products': [{'id': self.product.id, 'name': self.product.name, 'quantity': 1}]}
        session.save()

        #Se realiza la petición GET:
        request = self.factory.get(reverse('history'))
        request.user = self.user
        request.session = session
        response = shopping_history(request)
        self.assertEqual(response.status_code, 200)