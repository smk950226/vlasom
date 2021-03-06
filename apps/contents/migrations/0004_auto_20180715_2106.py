# Generated by Django 2.0.7 on 2018-07-15 12:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contents', '0003_contents_like_count'),
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
        migrations.AddField(
            model_name='contents',
            name='like',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL, verbose_name='좋아요'),
        ),
        migrations.AlterField(
            model_name='contents',
            name='like_count',
            field=models.PositiveIntegerField(default=0, verbose_name='좋아요 수'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
