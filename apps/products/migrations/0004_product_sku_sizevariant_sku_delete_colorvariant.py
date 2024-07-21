# Generated by Django 4.2.14 on 2024-07-21 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_product_price_sizevariant_colorvariant'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(default='No sku', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sizevariant',
            name='sku',
            field=models.CharField(default='No SKU', max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ColorVariant',
        ),
    ]
