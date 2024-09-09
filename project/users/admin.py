from django.contrib import admin
from .models import UserProfile, UserFollowing

def mark_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['registration_timestamp', ]
    list_display = ['__str__', 'profile_name', 'phone', 'dob', 'registration_timestamp']
    list_filter = ['gender', 'registration_timestamp', ]
    search_fields = ['profile_name', 'user__first_name', 'user__last_name']
    actions = [mark_verified,]

    class Meta:
        model = UserProfile
        fields = '__all__'


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    readonly_fields = ['created']
    list_filter = ['user_id', 'following_user_id']
    class Meta:
        model = UserFollowing
        fields = '__all__'
