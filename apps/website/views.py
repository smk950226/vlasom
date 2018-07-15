from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.common.mixins import LoginRequiredMixin
from apps.contents.models import Contents


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'website/home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('website:landing')
        return super().dispatch(request, *args, **kwargs)

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