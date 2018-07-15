# Generated by Django 2.0.7 on 2018-07-15 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180715_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('F', '남성'), ('M', '여성')], default='F', max_length=2, verbose_name='성별'),
            preserve_default=False,
        ),
    ]
