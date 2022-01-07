# Generated by Django 3.0.7 on 2021-03-11 11:15

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_productfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/ajay/Dev/venv/myenv/src/static_cdn/protected_media'), upload_to=products.models.upload_product_file_loc),
        ),
    ]