from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'mobile_phone', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'mobile_phone')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('mobile_phone', 'avatar')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('mobile_phone', 'avatar')}),
    )
