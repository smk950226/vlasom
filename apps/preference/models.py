from django.db import models
from django.contrib.auth import get_user_model

from apps.contents.models import Contents, Category

User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(User, verbose_name = '회원', on_delete = models.CASCADE)
    contents = models.ForeignKey(Contents, verbose_name = '콘텐츠', default=None, on_delete = models.CASCADE)
    regist_dt = models.DateTimeField('작성 시각', auto_now_add = True)

    class Meta:
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'


class Interest(models.Model):
    user = models.ForeignKey(User, verbose_name = '회원', on_delete = models.CASCADE)
    contents = models.ForeignKey(Contents, verbose_name = '콘텐츠', default = None, blank = True, null = True, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, verbose_name = '카테고리', default = None, blank = True, null = True, on_delete = models.CASCADE)
    regist_dt = models.DateTimeField('작성 시각', auto_now_add = True)

    class Meta:
        verbose_name = '관심 목록'
        verbose_name_plural = '관심 목록'
