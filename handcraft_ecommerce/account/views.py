from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
# from django.shortcuts import render
# from datetime import datetime, timedelta
# from django.shortcuts import get_object_or_404, render
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password
# from rest_framework import status
# from .serializers import SignUpSerializer,UserSerializer
# from rest_framework.permissions import IsAuthenticated
# from django.utils.crypto import get_random_string
# from django.core.mail import send_mail
# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1), # expiration 1h
            'iat': datetime.datetime.utcnow() # tokenCreatedAt
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token  # Decode here if needed
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout success.'
        }
        return response

class allUsers(APIView):
    def get(self,request):
        users=User.usersList()
        dataJSON=UserSerializer(users,many=True).data
        return Response({'model':'User', 'Users':dataJSON}) 
    
# @api_view(['POST'])
# def register(request):
#     data = request.data
    
    
#     profile_data = {
#         'phone': data.get('phone', ''),
#         'usertype': data.get('usertype', ''),
#         'address': data.get('address', ''),
#         'shopname': data.get('shopname', ''),
#         'ssn' : data.get('ssn', '')
#     }
    
    
#     user_data = {
#         'first_name': data.get('first_name', ''),
#         'last_name': data.get('last_name', ''),
#         'username': data.get('username',''),
#         'email': data.get('email', ''),
#         'password': make_password(data.get('password', '')),  
#         'profile': profile_data  
#     }

#     user_serializer = SignUpSerializer(data=user_data)
    
#     if user_serializer.is_valid():
#         if not User.objects.filter(username=data['email']).exists():
#             user_instance = user_serializer.save()  

            
#             if user_instance.profile.usertype == 'vendor' and (not profile_data.get('shopname') or not profile_data.get('ssn')):
#                 return Response({'error': 'Shop name and ssn are required for vendors.'}, status=status.HTTP_400_BAD_REQUEST)


#             return Response({'details': 'Your account registered successfully!'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'This email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)