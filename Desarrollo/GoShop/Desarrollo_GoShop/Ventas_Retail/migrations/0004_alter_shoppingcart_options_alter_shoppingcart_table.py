# Generated by Django 4.2.1 on 2023-05-09 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas_Retail', '0003_remove_shoppingcart_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'cart', 'verbose_name_plural': 'carts'},
        ),
        migrations.AlterModelTable(
            name='shoppingcart',
            table='shopping_cart',
        ),
    ]