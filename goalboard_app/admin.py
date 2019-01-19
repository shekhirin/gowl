from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from goalboard_app.models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Spreadsheet ID', {
            'fields': ('spreadsheetId',)
        }),
        ('Is username set', {
            'fields': ('is_username_set',)
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)
