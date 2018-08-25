from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm, PasswordChangeForm as BasePasswordChangeForm
from django.utils.safestring import mark_safe
from allauth.socialaccount.forms import SignupForm as AllauthSignupForm
from allauth.socialaccount.adapter import get_adapter

from apps.common.validators import validate_password
from apps.common.utils import birth_year, birth_month, birth_day

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자, 특수기호(!@#$%^&*)를 혼합하여 사용하세요.'}), validators=[validate_password])
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'placeholder': ''}))
    is_agreed_1 = forms.BooleanField(label='약관동의')
    is_agreed_2 = forms.BooleanField(label='개인정보수집동의')

    current_site = None

    class Meta:
        model = User
        fields = [
            'login_id',
            'email',
            'name',
            'nickname',
            'gender',
            'birth_year',
            'birth_month',
            'birth_day',
            'password1',
            'password2',
            'is_agreed_1',
            'is_agreed_2',
        ]
        help_texts = {
            'email': 'VLASOM의 ID로 사용할 이메일 주소를 입력해주세요.<br>가입하신 이메일 주소는 변경할 수 없습니다.',
            'nickname': '닉네임은 언제든지 변경할 수 있습니다.'
        }
        widgets = {
            'login_id': forms.TextInput(attrs={'placeholder': '로그인 ID'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'name': forms.TextInput(attrs={'placeholder': '홍길동'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'Nickname'}),
            'gender': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        self.current_site = kwargs.pop('current_site')
        super().__init__(*args, **kwargs)


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class SocialSignupForm(AllauthSignupForm):
    nickname = forms.CharField(label = '닉네임', required=True, widget = forms.TextInput(attrs={'autocomplete': 'off'}))
    gender = forms.CharField(label = '성별', required=True, widget = forms.RadioSelect())
    birth_year = forms.IntegerField(label = '생년', required=True, widget = forms.Select(choices = birth_year))
    birth_month = forms.IntegerField(label = '생월', required=True, widget = forms.Select(choices = birth_month))
    birth_day = forms.IntegerField(label = '생일', required=True, widget = forms.Select(choices = birth_day))

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.save_user(request, self.sociallogin, form=self, commit=False)
        join_channel = self.sociallogin.account.get_provider().name.upper()
        
        user.join_channel = join_channel
        user.login_id = str(user.join_channel) + '_id_' + str(user.id)
        user.email = self.cleaned_data['email']
        user.gender = self.cleaned_data['gender']
        user.birth_year = self.cleaned_data['birth_year']
        user.birth_month = self.cleaned_data['birth_month']
        user.birth_day = self.cleaned_data['birth_day']
        user.nickname = self.cleaned_data['nickname']
        user.is_verified = True
        if join_channel == 'KAKAO':
            user.name = self.sociallogin.account.extra_data['properties']['nickname']

        user.save()
        self.custom_signup(request, user)
        return user

    def clean_nickname(self):
        value = self.cleaned_data['nickname']
        if value:
            value = self.validate_unique_nickname(value)
        return value

    def validate_unique_nickname(self, value):
        try:
            return get_adapter().validate_unique_nickname(value)
        except forms.ValidationError:
            raise forms.ValidationError(
                get_adapter().error_messages['nickname_taken'])


class UserUpdateForm(forms.ModelForm):
    login_id_readonly = forms.CharField(label='로그인 ID', widget=forms.TextInput(attrs={'readonly': ''}), required=False)
    email_readonly = forms.CharField(label='이메일', widget=forms.TextInput(attrs={'readonly': ''}), required=False)

    class Meta:
        model = User
        fields = [
            'login_id_readonly',
            'email_readonly',
            'name',
            'nickname',
            'gender',
            'profile_image',
            'birth_year',
            'birth_month',
            'birth_day',
        ]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['login_id_readonly'].initial = self.instance.login_id
        self.fields['email_readonly'].initial = self.instance.email

    def save(self, commit=True):
        instance = super(UserUpdateForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class UserVerifyForm(forms.Form):
    email = forms.EmailField(
        label='이메일', widget=forms.EmailInput(attrs={'readonly': 'readonly'}),
        help_text='회원가입을 완료한 시점에 위의 이메일 주소로 이메일 인증을 위한 링크를 발송했습니다.<br>만약 5분이 지나도 이메일이 오지 않는 경우에는 아래 재발송 버튼을 클릭하시거나 스팸 메일함을 확인하세요.'
    )

    def __init__(self, *args, **kwargs):
        email = kwargs.pop('email')
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = email


class SetPasswordForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자, 특수기호(!@#$%^&*)를 혼합하여 사용하세요.'}),
        validators=[validate_password],
        strip=False,
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        strip=False,
        widget=forms.PasswordInput,
    )


class PasswordChangeForm(BasePasswordChangeForm):
    old_password = forms.CharField(
        label='기존 비밀번호',
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자, 특수기호(!@#$%^&*)를 혼합하여 사용하세요.'}),
        strip=False,
        validators=[validate_password],
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        strip=False,
        widget=forms.PasswordInput,
    )