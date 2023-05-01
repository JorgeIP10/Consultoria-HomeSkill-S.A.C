from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, ProductCategory

class TestProductDescription(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_category = ProductCategory.objects.create(name='Kitchen')
        self.test_product = Product.objects.create(
            name='Kitchen Products',
            category=self.test_category,
            price=10.0,
            description='Test description'
        )

    def test_product_description_get(self):
        url = reverse('description', kwargs={'view_name': 'kitchen', 'product_id': self.test_product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_description.html')
        self.assertEqual(response.context['product'], self.test_product)
        self.assertEqual(response.context['previous_view'], 'Cocina')
        self.assertEqual(response.context['view'], 'kitchen')

    def test_product_description_get_wrong_product_id(self):
        url = reverse('description', kwargs={'view_name': 'kitchen', 'product_id': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_description.html')
        self.assertIsNone(response.context.get('product'))
        self.assertEqual(response.context['previous_view'], 'Cocina')
        self.assertEqual(response.context['view'], 'kitchen')