from django import forms
from .models import Contents, ContentsImage


class ContentsForm(forms.ModelForm):
    class Meta:
        model = Contents
        fields = ['category_1', 'category_2', 'tags', 'description']
        help_texts = {
            'tags': '원하는 태그를 자유롭게 추가해 보세요.',
            'description': '이 사진을 어떻게 찍었는지 간단한 설명을 해주세요.'
        }


class ContentsImageForm(forms.ModelForm):
    class Meta:
        model = ContentsImage
        fields = ['image']