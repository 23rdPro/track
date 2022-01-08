# flake8: noqa

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        'username', 'email', 'is_active',
        'id'
    )
    list_filter = ('is_staff', 'is_superuser',
                   'is_active', 'groups',
                   )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('name', )}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser',
                                       'is_active', 'groups',
                                       'user_permissions'
                                       )
                            }
         ),
        (_('Important dates'), {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'name', )
    ordering = ('email', 'username')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
