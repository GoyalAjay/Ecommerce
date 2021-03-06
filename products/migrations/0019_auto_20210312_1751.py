# Generated by Django 3.0.7 on 2021-03-12 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20210312_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productfile',
            options={'ordering': ['-name']},
        ),
        migrations.AlterField(
            model_name='productfile',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z ]+$', 'Just type the name. Extension will be add automatically')]),
        ),
    ]
