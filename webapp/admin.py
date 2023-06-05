from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password

from .models import Users, BankDetails


class CustomUserAdmin(UserAdmin):
    authentication_backends = ['webapp.myauthBackend.UserAuthBackend']
    list_display = ('username', 'password','is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),)
    def save_model(self, request, obj, form, change):
        # Hash the password if it is provided and not already hashed
        if form.cleaned_data.get('password') and not form.cleaned_data.get('password').startswith('pbkdf2_sha256$'):
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(BankDetails)
admin.site.register(Users, CustomUserAdmin)
