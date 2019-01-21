from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from goalboard_app.models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Goalboard', {
            'fields': ('spreadsheetId', 'is_username_set', 'is_spreadsheet_set', 'updated', 'spreadsheet_data')
        }),
    )
    readonly_fields = ('updated', )


admin.site.register(CustomUser, CustomUserAdmin)
