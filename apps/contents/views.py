import json
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from apps.common.mixins import LoginRequiredMixin
from .forms import ContentsCreateForm
from .models import Contents, ContentsImages

class ContentsCreate(LoginRequiredMixin, CreateView):
    template_name = 'contents/contents_create.html'
    form_class = ContentsCreateForm

    name = 'contents_create'

    def form_valid(self, form):
        contents = form.save(commit = False)
        contents.user = self.request.user
        contents.save()
        files = self.request.FILES.getlist('image')
        for f in files:
            ContentsImages.objects.create(user = self.request.user, image = f)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contents:contents_detail', kwargs={'pk': self.object.id})


class ContentsList(LoginRequiredMixin, ListView):
    template_name = 'contents/contents_list.html'
    paginate_by = 20

    name = 'contents_list'


    def get_queryset(self):
        return Contents.objects.all()


class ContentsDetail(LoginRequiredMixin, DetailView):
    template_name = 'contents/contents_detail.html'
    model = Contents

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views += 1
        self.object.save()
        return response

class ContentsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'contents/contents_update.html'
    form_class = ContentsCreateForm
    model = Contents
    success_message = '성공적으로 내 콘텐츠를 수정했습니다.'

    name = 'contents_update'

    def get_success_url(self):
        return reverse('contents:contents_detail', kwargs={'pk': self.object.id})