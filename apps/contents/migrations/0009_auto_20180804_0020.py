# Generated by Django 2.0.7 on 2018-08-03 15:20

import apps.common.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0008_auto_20180802_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentsimages',
            name='image',
            field=models.ImageField(upload_to=apps.common.utils.get_image_filename2, verbose_name='이미지'),
        ),
    ]
