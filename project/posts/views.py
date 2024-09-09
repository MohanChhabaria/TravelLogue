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

class IternaryDetails(APIView):
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
        travellor_profile = get_object_or_404(UserProfile, user = user)
        data['travellor'] = travellor_profile
        try:
            iternary = Iternary.objects.create(**data)
            iternary.save()
        except IntegrityError:
            return Response({'Error': 'Invalid/Empty Fields in Form'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(IternarySerializer(iternary).data, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        travellor = get_object_or_404(UserProfile, user = user)
        iternaries = Iternary.objects.filter(travellor = travellor)
        serializer = IternarySerializer(iternaries, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    

    def delete(self, request, *args, **kwargs):
        data = {}
        for key in request.data.keys():
            if request.data.get(key) != '':
                if request.data.get(key) == 'true':
                    data[key] = True
                elif request.data.get(key) == 'false':
                    data[key] = False
                else:
                    data[key] = request.data.get(key)
        
        if(data['id']==None):
            return Response({'Error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        iternary = Iternary.objects.get(pk = data['id'])
        user = request.user
        travellor_profile = get_object_or_404(UserProfile, user = user)
        if iternary.travellor!=travellor_profile:
            return Response({'Error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        
        operation = iternary.delete()
        data = {}
        if operation:
            data["operation status"] = "Successfully deleted post"
        else:
            data["operation status"] = "Failed to delete post"
        return Response(data=data)
    

class AddDestinationView(APIView):

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
        
        # user = request.user
        iternary = get_object_or_404(Iternary, pk = data['id'])
        data['iternary'] = iternary
        data.pop("id")
        try:
            destination = Destination.objects.create(**data)
            destination.save()
        except IntegrityError:
            return Response({'Error': 'Invalid/Empty Fields in Form'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(DestinationSerializer(destination).data, status=status.HTTP_200_OK)


class GetAllDestinationsDetails(APIView):

    def get(self, request,id, *args, **kwargs):
        # user = request.user
        iternary = get_object_or_404(Iternary, pk = id)
        destinations = Destination.objects.filter(iternary = iternary)
        serializer = DestinationSerializer(destinations, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    

class GetDestinationDetails(APIView):

    def get(self, request,id, *args, **kwargs):

        destination = get_object_or_404(Destination, pk = id)
        serializer = DestinationSerializer(destination)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request,*args, **kwargs):
        data = {}
        for key in request.data.keys():
            if request.data.get(key) != '':
                if request.data.get(key) == 'true':
                    data[key] = True
                elif request.data.get(key) == 'false':
                    data[key] = False
                else:
                    data[key] = request.data.get(key)
        
        if(data['id']==None):
            return Response({'Error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        destination = Destination.objects.get(pk = data['id'])

        operation = destination.delete()
        data = {}
        if operation:
            data["operation status"] = "Successfully deleted post"
        else:
            data["operation status"] = "Failed to delete post"
        return Response(data=data)
    


class AddAccomodation(APIView):

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
        destination = get_object_or_404(Destination, pk = data['id'])
        data['destination'] = destination
        try:
            accomodation = Accomodation.objects.create(**data)
            accomodation.save()
        except IntegrityError:
            return Response({'Error': 'Invalid/Empty Fields in Form'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(AccomodationSeralizer(destination).data, status=status.HTTP_200_OK)

class AllAccomodationDetails(APIView):

    def get(self, request,id, *args, **kwargs):
        # user = request.user
        destination = get_object_or_404(Destination, pk = id)
        accomodations = Accomodation.objects.filter(destination = destination)
        serializer = AccomodationSeralizer(accomodations, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class AccomodationDetails(APIView):

    def get(self, request,id, *args, **kwargs):
        # user = request.user
        accomodation = get_object_or_404(Accomodation, pk = id)
        serializer = AccomodationSeralizer(accomodation)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        data = {}
        for key in request.data.keys():
            if request.data.get(key) != '':
                if request.data.get(key) == 'true':
                    data[key] = True
                elif request.data.get(key) == 'false':
                    data[key] = False
                else:
                    data[key] = request.data.get(key)
        
        if(data['id']==None):
            return Response({'Error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        accomodation = Accomodation.objects.get(pk = data['id'])

        operation = accomodation.delete()
        data = {}
        if operation:
            data["operation status"] = "Successfully deleted post"
        else:
            data["operation status"] = "Failed to delete post"
        return Response(data=data)
    

class MediaAPIView(APIView):
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
        travellor = get_object_or_404(UserProfile, user= user)
        iternary = get_object_or_404(Iternary, pk = data['id'])
        data['iternary'] = iternary
        data['travellor'] = travellor
        data.pop('id')
        try:
            media = Media.objects.create(**data)
            media.save()
        except IntegrityError:
            return Response({'Error': 'Invalid/Empty Fields in Form'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(MediaSerializer(media).data, status=status.HTTP_200_OK)
    

class GetIternaryMediaAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,id, *args, **kwargs):
        iternary = get_object_or_404(Iternary, pk = id)
        media = Media.objects.filter(iternary=iternary)
        serializer = MediaSerializer(media, many = True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class GetMediaAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, *args, **kwargs):
        media = get_object_or_404(Media, pk = id)
        serializer = MediaSerializer(media)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        data = {}
        for key in request.data.keys():
            if request.data.get(key) != '':
                if request.data.get(key) == 'true':
                    data[key] = True
                elif request.data.get(key) == 'false':
                    data[key] = False
                else:
                    data[key] = request.data.get(key)
        
        if(data['id']==None):
            return Response({'Error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        media = Media.objects.get(pk = data['id'])

        operation = media.delete()
        data = {}
        if operation:
            data["operation status"] = "Successfully deleted post"
        else:
            data["operation status"] = "Failed to delete post"
        return Response(data=data)



