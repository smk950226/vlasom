from django.contrib import messages
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView as BasePasswordResetConfirmView, \
    PasswordChangeView as BasePasswordChangeView, PasswordResetView as BasePasswordResetView, login as auth_login2
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, UpdateView, FormView, TemplateView
from django.conf import settings

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from allauth.socialaccount.views import SignupView

from .forms import UserCreateForm, UserUpdateForm, UserVerifyForm, SetPasswordForm, PasswordChangeForm
from apps.common.mixins import LoginRequiredMixin
from apps.contents.models import Category, Contents
from apps.preference.models import Interest

User = get_user_model()

def login(request):
    providers = []
    for provider in get_providers():
        try:
            provider.social_app = SocialApp.objects.get(provider = provider.id, sites = settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login2(request,
        template_name = 'accounts/login.html',
        extra_context = {'providers' : providers})

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_menu'] = Category.objects.all()
        context['interest_category'] = Interest.objects.filter(user = self.request.user, contents__isnull = True)
        context['interest_contents'] = Interest.objects.filter(user = self.request.user, category__isnull = True)
        context['upload_list'] = Contents.objects.filter(user = self.request.user)
        return context
    

class UserCreate(CreateView):
    template_name = 'registration/user_create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('user_verify')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_site'] = get_current_site(self.request)
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        auth_login(self.request, user)
        user.send_verification_email(get_current_site(self.request))

        return response


class UserVerify(SuccessMessageMixin, FormView):
    template_name = 'registration/verify/user_verify.html'
    model = User
    form_class = UserVerifyForm
    success_url = reverse_lazy('user_verify')
    success_message = '인증 이메일을 전송하였습니다.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['email'] = self.request.user.email
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.send_verification_email(get_current_site(self.request))
        return response

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse('login')
        return super().dispatch(request, *args, **kwargs)


class UserConfirm(RedirectView):
    token_generator = default_token_generator
    user = None
    success_message = '성공적으로 이메일 인증이 완료되었습니다.'

    def get_redirect_url(self, *args, **kwargs):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        user_id = urlsafe_base64_decode(uidb64).decode()
        self.user = get_object_or_404(User, pk=user_id)

        if self.token_generator.check_token(self.user, token):
            self.user.is_verified = True
            self.user.save()
            messages.success(self.request, self.success_message)
        return reverse('website:home')


class UserUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'registration/user_update.html'
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy('profile')
    success_message = '성공적으로 내 정보를 저장했습니다.'

    name = 'user_update'

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_menu'] = Category.objects.all()
        return context
    


class PasswordResetView(BasePasswordResetView):
    html_email_template_name = 'registration/password_reset_email.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    form_class = SetPasswordForm


class PasswordChangeView(BasePasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    name = 'password_change'


class FindId(TemplateView):
    template_name = 'accounts/find_id.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get('name', '')
        email = self.request.GET.get('email', '')
        if name and email:
            context['result_step'] = True
            if User.objects.filter(name = name, email = email):
                context['result'] = User.objects.filter(name = name, email = email).first().login_id
        return context