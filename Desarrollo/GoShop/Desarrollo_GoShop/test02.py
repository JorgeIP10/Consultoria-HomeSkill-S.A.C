from django.test import TestCase
from django.urls import reverse
from .models import Product, ProductCategory


class ProductTests(TestCase):
    def setUp(self):
        test_category = ProductCategory.objects.create(name='Kitchen')
        Product.objects.create(category=test_category, name='Kitchen Products', price=10.00, stock=5)

    def test_products_view(self):
        url = reverse('products', kwargs={'text': 'Kitchen'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kitchen Products')

    def test_products_search(self):
        category = ProductCategory.objects.create(name='test_category')
        Product.objects.create(name='Product 1', category=category, description='Product 1 description',price=5.99)
        Product.objects.create(name='Product 2', category=category, description='Product 2 description', price=10.80)
        url = reverse('products', kwargs={'text': 'Product'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')
