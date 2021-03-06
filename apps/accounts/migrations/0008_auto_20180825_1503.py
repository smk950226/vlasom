# Generated by Django 2.0.7 on 2018-08-25 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20180815_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='join_channel',
            field=models.CharField(choices=[('WEB', 'WEB'), ('KAKAO', 'KAKAO'), ('FACEBOOK', 'FACEBOOK'), ('GOOGLE', 'GOOGLE')], default='WEB', max_length=10, verbose_name='접속 채널'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.PositiveIntegerField(choices=[(1, '1일'), (2, '2일'), (3, '3일'), (4, '4일'), (5, '5일'), (6, '6일'), (7, '7일'), (8, '8일'), (9, '9일'), (10, '10일'), (11, '11일'), (12, '12일'), (13, '13일'), (14, '14일'), (15, '15일'), (16, '16일'), (17, '17일'), (18, '18일'), (19, '19일'), (20, '20일'), (21, '21일'), (22, '22일'), (23, '23일'), (24, '24일'), (25, '25일'), (26, '26일'), (27, '27일'), (28, '28일'), (29, '29일'), (30, '30일'), (31, '31일')], default=25, verbose_name='생일'),
        ),
    ]
