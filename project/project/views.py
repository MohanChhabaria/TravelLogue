import jwt
import datetime
import requests

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


from decouple import config

SECRET_KEY = config('SECRET_KEY', cast=str)

class Login(views.APIView):

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide email/password"}, status="400", content_type="application/json")

        email = request.data['email']
        password = request.data['password']
        users = User.objects.filter(email=email)
        if len(users) > 1:
            user = User.objects.filter(email=email, is_superuser=True)[0]
        elif len(users) == 1:
            user = users[0]
        else:
            return Response(
                {'Error': "Invalid credentials"},
                status=400,
                content_type="application/json"
            )
        if user and user.check_password(password):

            payload = {
                'id': user.id,
                'email': user.email,
                'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
            }
            data = {'token': jwt.encode(payload, SECRET_KEY, algorithm="HS256")}
            
            data['Dname'] = user.email
            return Response(
                data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                {'Error': "Invalid credentials"},
                status=400,
                content_type="application/json"
            )


class GoogleLogin(views.APIView):

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide the token"}, status="400")

        token = request.data['token']
        resp = requests.post('https://oauth2.googleapis.com/tokeninfo', data={'id_token': token})
        data = resp.json()
        if not data['email'] or resp.status != 200:
            return Response(
                {'Error': "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(email=data['email']).first()
        if user is None:
            user = User.objects.create_user(
                email=data["email"], username=data["name"])
        if user:

            payload = {
                'id': user.id,
                'email': user.email,
                'exp': datetime.now() + datetime.timedelta(hours=24)
            }
            jwt_token = {'token': jwt.encode(payload, SECRET_KEY, algorithm="HS256")}

            return Response(
                jwt_token,
                status=status.HTTP_200_OK)
