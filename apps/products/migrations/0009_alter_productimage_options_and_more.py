# Generated by Django 4.2.14 on 2024-07-28 08:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_productvariant_varient_sku'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['created_at']},
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='is_feature',
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='varient_sku',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='SKU must contain only letters, numbers, hyphens, and underscores.', regex='^[a-zA-Z0-9_-]*$')]),
        ),
    ]
