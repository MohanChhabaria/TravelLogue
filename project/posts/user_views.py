from django.shortcuts import render
from .models import Iternary,Destination, Accomodation, Media
from users.models import User, UserProfile, UserFollowing
from users.serializers import UserFollowingSerializer,  UserProfileSerializer, UserSerializer
from .serializers import AccomodationSeralizer, DestinationSerializer, MediaSerializer, IternarySerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class ContentPaginator(LimitOffsetPagination):
    default_limit = 1
    max_limit = 100 


class SearchTravellor(APIView):
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

        user = request.user
        if(data['name']==None):
            return Response({'Error': 'Invalid/Empty Fields in Form'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['name'] = (data['name']).lower()
        travellor_profiles = UserProfile.objects.filter(profile_name__contains=data['name'])
        serializer = UserProfileSerializer(travellor_profiles, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
class FetchTravellorDetails(APIView):

    def get(self, request, id,  *args, **kwargs):
        
        user = request.user
        data = {}
        req_user  = User.objects.get(pk = id)

        if(not req_user):
            return Response({'Error': 'Profile not found'}, status=status.HTTP_400_BAD_REQUEST)
        isfollowing = UserFollowing.objects.filter(user_id = user.id, following_user_id = req_user.id)
        profile = UserProfile.objects.get(user = req_user)
        serializer = UserProfileSerializer(profile)
        data['profile'] = serializer.data
        data['is_following'] = False
        if len(isfollowing)==0:
            return Response({'context':data}, status=status.HTTP_200_OK)
        
        data['is_following'] = True
        return Response({'context':data}, status=status.HTTP_200_OK)

        

class FetchTravellorIternaries(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = ContentPaginator
        
    def get(self, request,id, *args, **kwargs):

        req_user  = User.objects.get(pk = id)
        profile = UserProfile.objects.get(user = req_user)
        iternaries = Iternary.objects.filter(travellor = profile.id)
        paginator = self.pagination_class()
        result = paginator.paginate_queryset(iternaries, request)
        serializer = IternarySerializer(result, many=True)
        response_data = paginator.get_paginated_response(serializer.data)
        return Response(response_data.data, status=status.HTTP_200_OK)


class SearchIternary(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = ContentPaginator
    
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

        
        if(data['place']==None):
            return Response({'Error': 'Invalid/Empty Fields in Form'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['place'] = (data['place']).lower()
        iternaries = Iternary.objects.filter(title__contains=data['place'])
        paginator = self.pagination_class()
        result = paginator.paginate_queryset(iternaries, request)
        serializer = IternarySerializer(result, many=True)
        response_data = paginator.get_paginated_response(serializer.data)
        return Response(response_data.data, status=status.HTTP_200_OK)


class GetAllIternariesAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = ContentPaginator

    def get(self, request, *args, **kwargs):
        #  some logic 
        queryset = Iternary.objects.all().order_by('-registration_timestamp')
        paginator = self.pagination_class()
        result = paginator.paginate_queryset(queryset, request)
        serializer = IternarySerializer(result, many=True)
        response_data = paginator.get_paginated_response(serializer.data)
        return Response(response_data.data, status=status.HTTP_200_OK)
       




        
        