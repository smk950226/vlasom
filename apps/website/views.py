from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.common.mixins import LoginRequiredMixin
from apps.common.views import SearchView
from apps.contents.models import Contents, Category
from apps.preference.models import Interest

from .models import Terms


class HomeView(LoginRequiredMixin, SearchView):
    template_name = 'website/home.html'

    model = Contents

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('website:landing')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_contents'] = Contents.objects.all().order_by('-like_count')[:12]
        context['new_contents'] = Contents.objects.all().order_by('-regist_dt')
        context['category_menu'] = Category.objects.all()
        context['category_list'] = Interest.objects.filter(user = self.request.user, contents__isnull=True)
        i = 1
        for category in context['category_list']:
            category_num = 'category_' + str(i)
            i += 1
            context[category_num] = Contents.objects.filter(category_1 = category.category)[:8]
        return context
    

class LandingView(TemplateView):
    template_name = 'website/landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('website:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_contents'] = Contents.objects.all().order_by('-like_count')[:27]
        return context


class SearchResult(LoginRequiredMixin, SearchView):
    model = Contents
    template_name = 'website/home.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_menu'] = Category.objects.all()
        return context
    

class TermView(TemplateView):
    template_name = 'website/terms.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path == '/terms/access/':
            category = 1
        elif self.request.path == '/terms/information/':
            category = 2

        context['description'] = Terms.objects.get(category = category).description
        if category == 1:
            context['category'] = '이용약관'
        elif category == 2:
            context['category'] = '개인정보처리방침'

        return context


class SearchTagView(LoginRequiredMixin, TemplateView):
    template_name = 'website/search.html'