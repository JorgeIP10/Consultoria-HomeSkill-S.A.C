from django.apps import AppConfig

class PaymentgatewayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PaymentGateway'

    def ready(self):
        import PaymentGateway.hooks