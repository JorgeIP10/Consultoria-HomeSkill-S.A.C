# Generated by Django 4.1.7 on 2023-04-26 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas_Retail', '0006_alter_product_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=20),
        ),
    ]
