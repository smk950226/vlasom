from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
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
