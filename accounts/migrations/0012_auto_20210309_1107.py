# Generated by Django 3.0.7 on 2021-03-09 11:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210309_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=None, max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+91 9999999999'. Up to 10 digits allowed.", regex='^\\+?1?\\d{1,10}$')]),
            preserve_default=False,
        ),
    ]
