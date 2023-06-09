from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea, TextInput

# Register your models here.
from .models import NewUser


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'is_active', 'is_staff', 'is_superuser')
    # prepopulated_fields = {'slug': ('first_name',)}
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
        ('Personal', {'fields': ('about',)}),
    )
    
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
        
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}),
    )


admin.site.register(NewUser, UserAdminConfig)