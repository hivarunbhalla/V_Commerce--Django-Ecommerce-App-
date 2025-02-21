# Generated by Django 4.2.14 on 2024-07-28 08:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productvariant_varient_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='varient_sku',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='SKU must contain only letters, numbers, hyphens, and underscores.', regex='^[a-zA-Z0-9_-]*$')]),
        ),
    ]
