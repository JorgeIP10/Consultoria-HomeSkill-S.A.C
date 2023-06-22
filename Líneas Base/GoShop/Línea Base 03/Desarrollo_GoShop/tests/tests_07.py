from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from Ventas_Retail.models import Product, ProductCategory
from django.urls import reverse
from ShoppingCart.views_shopping_cart import shopping_cart, get_product_quantity_cart, add_product, remove_product_unit, remove_product
from UserProfile.views_profile import user_profile, user_config, confirm_user_config, shopping_history

class ShoppingCartViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='testpass')
        self.client = Client()
        self.category = ProductCategory.objects.create(name='Test Category')
        self.product = Product.objects.create(
            id=1, name='TestProduct', price=100.0, category_id =self.category)

    def test_shopping_cart(self):
        request = self.factory.get(reverse('cart'))
        request.user = self.user
        response = shopping_cart(request)
        self.assertEqual(response.status_code, 200)

    def test_get_product_quantity_cart(self):
        request = self.factory.get(reverse('get_product_quantity_cart', args=[self.product.id]))
        request.user = self.user
        response = get_product_quantity_cart(request, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        request = self.factory.get(reverse('add_product', args=[self.product.id]))
        request.user = self.user
        response = add_product(request, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_remove_product_unit(self):
        request = self.factory.get(reverse('remove_product_unit', args=[self.product.id]))
        request.user = self.user
        response = remove_product_unit(request, self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_remove_product(self):
        request = self.factory.get(reverse('remove_product', args=[self.product.id]))
        request.user = self.user
        response = remove_product(request, self.product.id)
        self.assertEqual(response.status_code, 200)

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
        request = self.factory.get(reverse('confirm_user_config', kwargs={'previous_view': 'config', 'previous_name': 'Config', 'mode': 'username'}))
        request.user = self.user
        response = confirm_user_config(request, 'config', 'Config', 'username')
        self.assertEqual(response.status_code, 200)

    def test_shopping_history(self):
        session = self.client.session
        session['cart'] = {'products': [{'id': self.product.id, 'name': self.product.name, 'quantity': 1}]}
        session.save()

        request = self.factory.get(reverse('history'))
        request.user = self.user
        request.session = session
        response = shopping_history(request)
        self.assertEqual(response.status_code, 200)