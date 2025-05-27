from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import User, Profile


@admin.register(User)
class UserAdmin(ModelAdmin):
    model = User

    list_display = (
        'username', 'email', 'email_verified', 'is_active', 'is_staff', 'is_superuser', 'created',
    )

    list_filter = (
        'is_active', 'is_staff', 'email_verified',
    )

    search_fields = ('username', 'email')


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    model = Profile

    list_display = ('user', 'display_name')
