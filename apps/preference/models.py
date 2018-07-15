from django.db import models
from django.contrib.auth import get_user_model

from apps.contents.models import Contents

User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(User, verbose_name = '회원', on_delete = models.CASCADE)
    contents = models.ForeignKey(Contents, verbose_name = '콘텐츠', default=None, on_delete = models.CASCADE)
    regist_dt = models.DateTimeField('작성 시각', auto_now_add = True)

    class Meta:
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'
