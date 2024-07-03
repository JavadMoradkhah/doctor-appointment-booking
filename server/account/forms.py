from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["phone", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "is_active", "role"]
