from django.contrib import admin
from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email")
    list_display_links = ("id", "first_name")
