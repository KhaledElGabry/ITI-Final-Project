from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
# Create your views here.


@api_view(['POST'])
def register(request):
    data = request.data
    
    
    profile_data = {
        'phone': data.get('phone', ''),
        'usertype': data.get('usertype', ''),
        'address': data.get('address', ''),
        'shopname': data.get('shopname', ''),
        'ssn' : data.get('ssn', '')
    }
    
    
    user_data = {
        'first_name': data.get('first_name', ''),
        'last_name': data.get('last_name', ''),
        'username': data.get('username',''),
        'email': data.get('email', ''),
        'password': make_password(data.get('password', '')),  
        'profile': profile_data  
    }

    user_serializer = SignUpSerializer(data=user_data)
    
    if user_serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user_instance = user_serializer.save()  

            
            if user_instance.profile.usertype == 'vendor' and (not profile_data.get('shopname') or not profile_data.get('ssn')):
                return Response({'error': 'Shop name and ssn are required for vendors.'}, status=status.HTTP_400_BAD_REQUEST)


            return Response({'details': 'Your account registered successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'This email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)