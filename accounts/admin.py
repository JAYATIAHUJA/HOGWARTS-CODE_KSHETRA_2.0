from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SellerKYC

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_verified_seller', 'is_staff')
    list_filter = ('user_type', 'is_verified_seller', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_picture')}),
        ('Business info', {'fields': ('business_name', 'gstin', 'business_description')}),
        ('Permissions', {'fields': ('user_type', 'is_verified_seller', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    search_fields = ('username', 'email', 'business_name')
    ordering = ('username',)

class SellerKYCAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_status', 'submitted_at', 'verified_at')
    list_filter = ('verification_status',)
    search_fields = ('user__username', 'user__email', 'user__business_name')
    readonly_fields = ('submitted_at',)
    
    def save_model(self, request, obj, form, change):
        if 'verification_status' in form.changed_data:
            if obj.verification_status == 'VERIFIED':
                obj.user.is_verified_seller = True
            else:
                obj.user.is_verified_seller = False
            obj.user.save()
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SellerKYC, SellerKYCAdmin)
