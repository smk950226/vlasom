# Generated by Django 2.0.7 on 2018-08-26 06:55

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(1, '이용약관'), (2, '개인정보처리방침')], verbose_name='종류')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='내용')),
            ],
            options={
                'verbose_name': '약관',
                'verbose_name_plural': '약관',
            },
        ),
    ]