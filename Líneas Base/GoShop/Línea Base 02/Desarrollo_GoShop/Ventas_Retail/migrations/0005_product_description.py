# Generated by Django 4.1.7 on 2023-04-26 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas_Retail', '0004_alter_product_sale_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
