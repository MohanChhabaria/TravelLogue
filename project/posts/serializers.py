from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile, UserFollowing, User
from .models import Iternary, Destination, Accomodation, Media
from users.serializers import UserProfileSerializer

class IternarySerializer(serializers.ModelSerializer):
    travellor = UserProfileSerializer(read_only=True)

    class Meta:
        model = Iternary
        fields = ('title', 'travellor','no_of_days','description','expenditure')


class DestinationSerializer(serializers.ModelSerializer):
    iternary = IternarySerializer(read_only = True)

    class Meta:
        model = Destination
        fields = ('name', 'description','starting_day','iternary')


class AccomodationSeralizer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)

    class Meta:
        model = Accomodation
        fields = ('property_name', 'location', 'price','review', 'destination')


class MediaSerializer(serializers.ModelSerializer):
    iternary = IternarySerializer(read_only=True)
    
    class Meta:
        model = Media
        fields = ('iternary','title','media','uploaded_at')