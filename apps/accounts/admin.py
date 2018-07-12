from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()


class UserCreateAdminForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['login_id', 'email', 'password1', 'password2']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'login_id', 'email', 'nickname', 'is_verified', 'is_staff']
    list_display_links = ['id', 'login_id']
    list_filter = ['is_verified', 'is_active']
    ordering = ['-id']
    search_fields = ['login_id', 'email', 'nickname']
    add_form = UserCreateAdminForm
    add_form_template = 'admin/change_form.html'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login_id', 'email', 'name', 'nickname', 'birth_year', 'birth_month', 'birth_day', 'password1', 'password2', 'is_verified'),
        }),
    )
    fieldsets = [
        ('개인정보', {'fields': [
            'login_id',
            'name',
            'nickname',
            'email',
            'birth_year',
            'birth_month',
            'birth_day',
            'is_verified',
        ]}),
        ('권한', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'password'
        )})
    ]
