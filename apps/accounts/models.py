from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils import six, timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator

from apps.common.utils import birth_year, birth_month, birth_day, join_channel, gender_choice, profile_image_upload_to


class UserManager(BaseUserManager):
    def create_user(self, login_id, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(login_id=login_id, email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id, email, password):
        user = self.create_user(
            login_id,
            email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    login_id = models.CharField(
        _('로그인 ID'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("ID가 중복됩니다."),
        },
    )
    name = models.CharField('이름', max_length=20)
    nickname = models.CharField('닉네임', max_length=50, unique = True)
    email = models.EmailField('이메일', unique=True)
    gender = models.CharField('성별', max_length=2, choices = gender_choice)
    birth_year = models.PositiveIntegerField('생년', choices = birth_year, default = int(timezone.now().strftime("%Y")))
    birth_month = models.PositiveIntegerField('생월', choices = birth_month, default = int(timezone.now().strftime("%m")))
    birth_day = models.PositiveIntegerField('생일', choices = birth_day, default = int(timezone.now().strftime("%d")))
    is_verified = models.BooleanField('인증여부', default=False, help_text='사용자의 이메일 인증 여부를 나타냅니다.')
    profile_image = models.ImageField('프로필 사진', upload_to = profile_image_upload_to, blank = True, null = True)
    join_channel = models.CharField('접속 채널', max_length = 10,choices = join_channel, default = 'WEB')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = '회원'
        verbose_name_plural = '회원'

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def send_verification_email(self, current_site):
        uid = urlsafe_base64_encode(force_bytes(self.pk)).decode()
        token = default_token_generator.make_token(self)

        url = 'https://{}/accounts/signup/confirm/{}/{}/'.format(current_site.domain, uid, token)

        email_subject = render_to_string('registration/verify/user_verify_subject.txt')
        email_content = render_to_string('registration/verify/user_verify_email.html', context={'url': url, 'site_name': current_site.name})

        self.email_user(email_subject, '', html_message=email_content)
