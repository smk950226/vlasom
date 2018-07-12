from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView as BasePasswordResetConfirmView, \
    PasswordChangeView as BasePasswordChangeView, PasswordResetView as BasePasswordResetView, login as auth_login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, UpdateView, FormView
from django.conf import settings

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from allauth.socialaccount.views import SignupView

from .forms import UserCreateForm, UserUpdateForm, UserVerifyForm, SetPasswordForm, PasswordChangeForm
from .mixins import LoginRequiredMixin

User = get_user_model()

def login(request):
    providers = []
    for provider in get_providers():
        try:
            provider.social_app = SocialApp.objects.get(provider = provider.id, sites = settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login(request,
        template_name = 'accounts/login.html',
        extra_context = {'providers' : providers})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

class UserCreate(CreateView):
    template_name = 'accounts/registration/user_create.html'
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
    template_name = 'accounts/registration/verify/user_verify.html'
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
        return reverse('home')


class UserUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/registration/user_update.html'
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy('user_update')
    success_message = '성공적으로 내 정보를 저장했습니다.'

    name = 'user_update'

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(BasePasswordResetView):
    html_email_template_name = 'accounts/registration/password_reset_email.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    form_class = SetPasswordForm


class PasswordChangeView(BasePasswordChangeView):
    form_class = PasswordChangeForm

    name = 'password_change'
