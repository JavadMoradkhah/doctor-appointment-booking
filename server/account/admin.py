from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["phone", "is_active", "role"]
    list_filter = ["is_active", "role"]
    list_per_page = 10

    fieldsets = [
        (None, {"fields": ["phone"]}),
        ("نوع کاربر", {"fields": ['role']}),
    ]

    add_fieldsets = [
        (None, {"fields": ["phone"]}),
        ("نوع کاربر", {"fields": ['role']}),
    ]

    search_fields = ["phone"]
    ordering = ["phone"]
    filter_horizontal = []
