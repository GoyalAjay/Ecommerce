# Generated by Django 3.0.7 on 2021-03-15 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20210312_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_by',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
