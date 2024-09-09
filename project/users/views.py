from django.shortcuts import render
from .models import User, UserFollowing , UserProfile
from .serializers import UserFollowingSerializer,  UserProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework.response import Response
import json

class UserDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {}
        for key in request.data.keys():
            if request.data.get(key) != '':
                if request.data.get(key) == 'true':
                    data[key] = True
                elif request.data.get(key) == 'false':
                    data[key] = False
                else:
                    data[key] = request.data.get(key)
        
        email = data.pop('email')
        password = data.pop('password')
        data.pop('cpassword')
        first_name = data.pop("first_name")
        last_name = data.pop("last_name")
        user_details = {
            'email': email,
            "first_name" : first_name,
            "last_name" : last_name,
            "password" : password,
            "username" : first_name + " " +  last_name
        }
        user = User.objects.create(**user_details)
        userprofiles = UserProfile.objects.filter(profile_name=data['profile_name'])
        if(len(userprofiles)>0):
            return Response({
                'Error' : "profile name already exists"},
                status=302
            )
        try:
            profile = UserProfile.objects.create(user=user, **data)
            profile.save()
        except IntegrityError:
            return Response({'Error': 'Invalid/Empty Fields in Form'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(UserProfileSerializer(profile).data, status=status.HTTP_200_OK)
    

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(profile)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    

    def put(self, request, *args, **kwargs):
        data = {}
        for key in request.data.keys():
            if request.data.get(key) != '':
                if request.data.get(key) == 'true':
                    data[key] = True
                elif request.data.get(key) == 'false':
                    data[key] = False
                else:
                    data[key] = request.data.get(key)
        
        user = request.user
        profile = UserProfile.objects.get(user = user)
        serializer = UserProfile(instance=profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        operation = profile.delete()
        data = {}
        if operation:
            data["operation status"] = "Successfully deleted user profile"
        else:
            data["operation status"] = "Failed to delete user profile"
        return Response(data=data)



class UserFollowingDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = {}
        for key in request.data.keys():
            if request.data.get(key) != '':
                if request.data.get(key) == 'true':
                    data[key] = True
                elif request.data.get(key) == 'false':
                    data[key] = False
                else:
                    data[key] = request.data.get(key)
        
        if data['following_user']==None:
            return Response({
                'error' : 'user does not exist'},
                status=400)
        
        user = request.user
        following_user_profile = get_object_or_404(UserProfile, profile_name = data['following_user'])
        following_user = following_user_profile.user
        
        # following_user = User.objects.filter( id = (data['following_user_id']).id)
        data['following_user_id'] = following_user
        data['user_id'] = user
        data.pop("following_user")
        if following_user:
            try:
                obj = UserFollowing.objects.create(**data)
                obj.save()
            except IntegrityError:
                return Response({'Error': 'Invalid/Empty Fields in Form'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(UserFollowingSerializer(obj).data, status=status.HTTP_200_OK)
    

    def get(self, request , *args, **kwargs):
        user = request.user
        following = UserFollowing.objects.filter(user_id = user)
        followers = UserFollowing.objects.filter(following_user_id = user)
        
        follower_list = []
        following_list = []
        for follower in followers:
            follower_list.append(follower.user_id)
        for follower in following:
            following_list.append(follower.following_user_id)
        serializer = UserSerializer(follower_list, many = True)
    
        data = {}
        data['followers'] = serializer.data
        serializer = UserSerializer(following_list, many = True)
        data['following'] = serializer.data
        return  Response(data, status=status.HTTP_200_OK)
    

    def delete(self, request, *args, **kwargs):
        user = request.user
        data = {}
        for key in request.data.keys():
            if request.data.get(key) != '':
                if request.data.get(key) == 'true':
                    data[key] = True
                elif request.data.get(key) == 'false':
                    data[key] = False
                else:
                    data[key] = request.data.get(key)

        if data['following_user']==None:
            return Response({
                'error' : 'user does not exist'},
                status=400)
        
        user = request.user
        following_user_profile = get_object_or_404(UserProfile, profile_name = data['following_user'])
        following_user = following_user_profile.user
        
        data['user_id'] = user
        obj = UserFollowing.objects.get(**data)
        operation = obj.delete()
        data = {}
        if operation:
            data["operation status"] = "Successfully unfollowed"
        else:
            data["operation status"] = "Failed to unfollow "
        return Response(data=data)



