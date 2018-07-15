from django.db import models
from django.contrib.auth import get_user_model

from apps.common.utils import get_image_filename

User = get_user_model()

class Category(models.Model):
    name = models.CharField('카테고리', max_length = 50)

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'

    def __str__(self):
        return self.name


class Contents(models.Model):
    user = models.ForeignKey(User, verbose_name = '회원', on_delete = models.CASCADE)
    category_1 = models.ForeignKey(Category, verbose_name = '카테고리 1', on_delete = models.CASCADE, related_name = 'contents_category_1')
    category_2 = models.ForeignKey(Category, verbose_name = '카테고리 2', on_delete = models.CASCADE, related_name = 'contents_category_2', blank = True, null = True)
    tags = models.CharField('태그', max_length = 200, blank = True, null = True)
    description = models.TextField('설명', blank = True, null = True)
    regist_dt = models.DateTimeField('작성 시각', auto_now_add = True)
    like = models.PositiveIntegerField('좋아요', default = 0)
    views = models.PositiveIntegerField('조회수', default = 0)

    class Meta:
        verbose_name = '콘텐츠'
        verbose_name_plural = '콘텐츠'

        def __str__(self):

            return self.user + self.category_1 + self.category_2


class ContentsImages(models.Model):
    contents = models.ForeignKey(Contents, verbose_name = '콘텐츠', default=None, on_delete = models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='이미지')