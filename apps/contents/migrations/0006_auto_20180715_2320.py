# Generated by Django 2.0.7 on 2018-07-15 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0005_auto_20180715_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='contents',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
