from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..models import UserProfile, PaymentCard
from django.urls import reverse

class PaymentMethodTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        # no need to create UserProfile here, it's automatically created


    def test_user_payment_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('payment'))  
        self.assertEqual(response.status_code, 200)

    def test_add_payment_method(self):
        self.client.login(username='testuser', password='12345')
        card_data = {'card': '1234567890123456', 'select-month': '12', 'select-year': '2030', 'cvv': '123'}
        response = self.client.post(reverse('add_payment_method'), card_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PaymentCard.objects.filter(owner_id=self.user.id, number=card_data['card']).exists())

    def test_remember_payment_method(self):
        self.client.login(username='testuser', password='12345')
        card = PaymentCard.objects.create(owner_id=self.user.id, number='1234567890123456', 
                                        expiration_month='12', expiration_year='2030', cvv='123')
        response = self.client.post(reverse('remember_payment_method'), {'remember-card': card.id})
        self.assertEqual(response.status_code, 200)
        card.refresh_from_db()
        self.assertTrue(card.remembered)

