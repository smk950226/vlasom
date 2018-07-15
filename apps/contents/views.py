import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from apps.common.mixins import LoginRequiredMixin
from .forms import ContentsCreateForm
from .models import Contents, Like

class ContentsCreate(LoginRequiredMixin, CreateView):
    template_name = 'contents/contents_create.html'
    form_class = ContentsCreateForm

    name = 'contents_create'

    def form_valid(self, form):
        contents = form.save(commit = False)
        contents.user = self.request.user
        contents.save()
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
    

@login_required
def like_create(request, pk):
    contents = get_object_or_404(Contents, id=pk)

    if Like.objects.filter(user = request.user).filter(contents = contents).exists():
        Like.objects.filter(user = request.user).filter(contents = contents).delete()
        contents.like_count = Like.objects.filter(user = request.user).filter(contents = contents).count()
        contents.save()
        message = '좋아요 취소.'
    else:
        Like.objects.create(user = request.user, contents = contents)
        contents.like_count = Like.objects.filter(user = request.user).filter(contents = contents).count()
        contents.save()
        message = '좋아요.'
    
    context = {'message': message,}

    return HttpResponse(json.dumps(context), content_type="application/json")
