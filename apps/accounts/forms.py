from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm, PasswordChangeForm as BasePasswordChangeForm
from django.utils.safestring import mark_safe

from apps.account.validators import validate_password

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자 혹은 [!@#$%^&*]를 혼합하여 사용하세요.'}), validators=[validate_password])
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'placeholder': ''}))
    is_agreed_1 = forms.BooleanField(label='약관동의'))
    is_agreed_2 = forms.BooleanField(label='개인정보수집동의'))

    current_site = None

    class Meta:
        model = User
        fields = [
            'login_id'
            'email',
            'name',
            'nickname',
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
            'login_id': forms.TextInput(attrs=('placeholder': '로그인 ID')),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'name': forms.TextInput(attrs={'placeholder': '홍길동'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'Nickname'}),
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


class UserUpdateForm(forms.ModelForm):
    login_id_readonly = forms.CharField(label='로그인 ID', widget=forms.TextInput(attrs={'readonly': ''}))
    email_readonly = forms.CharField(label='이메일', widget=forms.TextInput(attrs={'readonly': ''}))

    class Meta:
        model = User
        fields = [
            'login_id_readonly',
            'email_readonly',
            'name',
            'nickname',
            'birth_year',
            'birth_month',
            'birth_day',
        ]
        labels = {
            'name': '이름 변경',
            'nickname': '닉네임 변경',
            'birth': '생년월일 변경',
        }

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
        widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자 혹은 [!@#$%^&*]를 혼합하여 사용하세요.'}),
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
        widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자 혹은 [!@#$%^&*]를 혼합하여 사용하세요.'}),
        strip=False,
        validators=[validate_password],
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        strip=False,
        widget=forms.PasswordInput,
    )
