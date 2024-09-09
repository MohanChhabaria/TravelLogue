from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserFollowing, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserFollowingSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    following_user_id = UserSerializer(read_only = True)

    class Meta:
        model = UserFollowing
        fields = ("user_id", "following_user_id", "created")

class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    class Meta:
        model = UserFollowing
        fields = ("user_id", "following_user_id", "created")

    def get_following(self, obj):
        return FollowingSerializer(UserProfile.objects.filter(user=obj.user_id), many=True).data


class FollowersSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    class Meta:
        model = UserFollowing
        fields = ("id", "user_id", "created")
    
    def get_followers(self, obj):
        return FollowingSerializer(UserProfile.objects.filter(user=obj.id), many=True).data


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    # following = serializers.SerializerMethodField()
    # followers = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        # fields = ('user', 'profile_name', 'phone', 'dob', 'gender','is_verified','user_image',
        #           'registration_timestamp', 'following', 'followers')
        fields = ('user','profile_name','phone','dob','gender')

    # def get_following(self, obj):
    #     return FollowingSerializer(obj.following.all(), many=True).data

    # def get_followers(self, obj):
    #     return FollowersSerializer(obj.followers.all(), many=True).data
