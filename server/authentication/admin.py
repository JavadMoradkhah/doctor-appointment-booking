from django.contrib import admin
from .models import Otp, OtpBlacklist

@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "attempts", "first_attempt", "last_attempt", "expires_at")
    search_fields = ("phone",)
    list_filter = ("expires_at",)
    readonly_fields = ("first_attempt", "last_attempt")

@admin.register(OtpBlacklist)
class OtpBlacklistAdmin(admin.ModelAdmin):
    list_display = ("phone", "expires_at", "created_at")
    search_fields = ("phone",)
    list_filter = ("expires_at",)
    readonly_fields = ("created_at",)
