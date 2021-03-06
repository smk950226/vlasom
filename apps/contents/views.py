import json
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from apps.common.mixins import LoginRequiredMixin
from apps.preference.models import Like, Interest

from .forms import ContentsCreateForm, ContentsUpdateForm
from .models import Contents, ContentsImages, Category

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
            ContentsImages.objects.create(user = self.request.user, contents=contents, image = f)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contents:contents_detail', kwargs={'pk': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_menu'] = Category.objects.all()
        return context
    


class ContentsList(LoginRequiredMixin, ListView):
    template_name = 'contents/contents_list.html'
    paginate_by = 30

    name = 'contents_list'


    def get_queryset(self):
        if self.request.path == '/contents/hot/list/':
            return Contents.objects.all().order_by('-like_count')
        elif self.request.path == '/contents/new/list/':
            return Contents.objects.all().order_by('-regist_dt')
        elif self.request.path == '/contents/uploaded/':
            return Contents.objects.filter(user = self.request.user).order_by('-regist_dt')
        else:
            category = Category.objects.get(id = self.kwargs['category_id'])
            return Contents.objects.filter(category_1 = category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path == '/contents/hot/list/':
            context['category'] = '인기 콘텐츠'
        elif self.request.path == '/contents/new/list/':
            context['category'] = '최근 콘텐츠'
        elif self.request.path == '/contents/uploaded/':
            context['category'] = '업로드한 콘텐츠'
        else:
            context['category'] = Category.objects.get(id = self.kwargs['category_id'])
            if Interest.objects.filter(user = self.request.user, category = Category.objects.get(id = self.kwargs['category_id'])).exists():
                context['category_is_interested'] = True 
            else:
                context['category_is_interested'] = False
        context['category_menu'] = Category.objects.all()
        return context
    



class ContentsDetail(LoginRequiredMixin, DetailView):
    template_name = 'contents/contents_detail.html'
    model = Contents

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views += 1
        self.object.save()
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_menu'] = Category.objects.all()
        context['like_set_contents'] = list(Like.objects.filter(user = self.request.user).values_list('contents', flat=True)) 
        context['interest_set_contents'] = list(Interest.objects.filter(user = self.request.user).values_list('contents', flat=True)) 
        return context
    

class ContentsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'contents/contents_update.html'
    form_class = ContentsUpdateForm
    model = Contents
    success_message = '성공적으로 내 콘텐츠를 수정했습니다.'

    name = 'contents_update'

    def get_success_url(self):
        return reverse('contents:contents_detail', kwargs={'pk': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contents_images'] = ContentsImages.objects.filter(contents = self.kwargs['pk'])
        context['category_menu'] = Category.objects.all() 
        return context


def contents_delete(request, pk):
    try:
        Contents.objects.filter(id = pk).delete()
        message = '삭제하였습니다.'
    except:
        message = '오류가 발생하여 삭제하지 못하였습니다.'
    
    context = {'message': message}

    return HttpResponse(json.dumps(context), content_type="application/json")