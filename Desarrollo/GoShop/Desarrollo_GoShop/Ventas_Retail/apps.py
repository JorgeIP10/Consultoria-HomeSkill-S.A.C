from django.apps import AppConfig


class VentasRetailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Ventas_Retail'

    def ready(self):
        import Ventas_Retail.hooks
