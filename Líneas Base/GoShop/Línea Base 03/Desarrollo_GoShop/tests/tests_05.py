from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ShoppingCart.views_shopping_cart import shopping_cart, get_product_quantity_cart, add_product, remove_product_unit, remove_product
from Ventas_Retail.models import Product
from Ventas_Retail.models import ProductCategory


class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='testpass')
        self.client = Client()
        self.category = ProductCategory.objects.create(name='Test Category')
        self.product = Product.objects.create(
            id=1, name='TestProduct', price=100.0, category_id=self.category)

    def test_shopping_cart(self):
        request = self.factory.get(reverse('cart'))
        request.user = self.user
        response = shopping_cart(request)
        self.assertEqual(response.status_code, 200)

    def test_get_product_quantity_cart(self):
        request = self.factory.get(reverse('get_product_quantity_cart', args=[1]))
        request.user = self.user
        response = get_product_quantity_cart(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        request = self.factory.post(reverse('add_product', args=[1]))
        request.user = self.user
        response = add_product(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_remove_product_unit(self):
        request = self.factory.post(reverse('remove_product_unit', args=[1]))
        request.user = self.user
        response = remove_product_unit(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_remove_product(self):
        request = self.factory.post(reverse('remove_product', args=[1]))
        request.user = self.user
        response = remove_product(request, 1)
        self.assertEqual(response.status_code, 200)