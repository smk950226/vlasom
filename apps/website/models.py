from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Terms(models.Model):
    category = models.IntegerField('종류', choices=((1,'이용약관'),(2,'개인정보처리방침')))
    description = RichTextUploadingField('내용')

    class Meta:
        verbose_name = '약관'
        verbose_name_plural = '약관'