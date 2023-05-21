from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = NewUser
    ordering = ('-start_date',)
    search_fields = ('email', 'user_name', )
    list_filter = ('email', 'user_name', 'is_active', 'is_staff', 'is_employee',  'groups')
    list_display = ('email', 'user_name', 'is_active', 'is_staff', 'is_employee', 'class_group')
    fieldsets = (
        ('Viewing', {
            'fields': ('email', 'user_name')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_employee')
        }),
        ('Group Permissions', {
            # 'classes': ('collapse',),
            'fields': ('groups', ) # 'user_permissions',
        }),
    )
    add_fieldsets = (
        ('Adding', {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2')
         }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_employee', 'groups')
        })
    )
    def class_group(self, obj):
        """
            get group, separate by comma, and display empty string if user has no group
        """
        return ','.join([g.name for g in obj.groups.all()]) if obj.groups.count() else ''


admin.site.register(NewUser, UserAdminConfig)
