from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from .models import CustomToken
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import jwt
import datetime
from rest_framework import status
from .app import upload_photo,delete_photos
import os
from urllib.parse import unquote
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .tokens import account_activation_token  # You need to create this token generator
from django.core.mail import EmailMessage

from .utils import generate_verification_token
from django.utils.http import urlsafe_base64_decode


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token = generate_verification_token()
        user.verification_token = token
        user.save()

        # Send verification email
        send_verification_email(user)

        return Response({"message": "success"})


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        if not user.is_active:
            raise AuthenticationFailed('Please Active Email First!')

        response = Response()

        token, created = CustomToken.objects.get_or_create(user=user)
        token.save()

        response.data = {
            "message":"success",
            "token": token.key,
            "user": UserSerializer(user).data,
        }
        return response
    
class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # get user
    def get(self, request):
        try:
            user = User.objects.get(id = request.user.id)
                        
            # Check if the user's token has expired
            token = CustomToken.objects.get(user=user)
            
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
            
            return Response({'message': UserSerializer(user).data})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # delete user
    def delete(self, request):
        try:
            user = User.objects.get(id = request.user.id)

            # Check if the user's token has expired
            token = CustomToken.objects.get(user=user)
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
            
            user = User.userDelete(request.user.id)
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # update user
    def put(self, request):
        try:
            id = request.user.id
            user = User.objects.get(id=id)

            # Check if the user's token has expired
            token = CustomToken.objects.get(user=user)
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
            
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # if user send new image
            if 'image' in request.data and request.data['image'] is not None:
                
                # if user has already image on drive
                if serializer.validated_data.get('image') is not None:
                    delete_photos(f"{id}.png")
                           
                # upload new image
                media_folder = os.path.join(os.getcwd(), "media/users/images")
                # save new url
                Url_Image = upload_photo(os.path.join(media_folder, os.path.basename(serializer['image'].value)),f"{id}.png")
                user.imageUrl = Url_Image
                user.save()
                
                # remove image from server
                if os.path.exists(media_folder):
                    for file_name in os.listdir(media_folder):
                        file_path = os.path.join(media_folder, file_name)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                                print(f"Deleted: {file_path}")
                            else:
                                print(f"Skipped: {file_path} (not a file)")
                        except Exception as e:
                            print(f"Error deleting {file_path}: {e}")
                else:
                    print("Folder does not exist.")

            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response({'message': 'Data Updated Successfully', "user":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            token = CustomToken.objects.get(user=request.user)
            token.delete()
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed({"message":'user is already logged out.'})

        response = Response({'message': 'Logout success.'}, status=status.HTTP_200_OK)
        return response

class allUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser & IsAuthenticated]

    def get(self,request):
        # Check if the user's token has expired
        try:
            user = get_object_or_404(User, id=request.user.id)
            token = CustomToken.objects.get(user=user)
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed({"data": "missing_token", "message": 'Token not found for the user.'})

        users=User.usersList()
        dataJSON=UserSerializer(users,many=True).data
        return Response({'Users':dataJSON})
    
    def delete(self, request):
        # Check if the user's token has expired
        try:
            user = get_object_or_404(User, id=request.user.id)
            token = CustomToken.objects.get(user=user)
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed({"data": "missing_token", "message": 'Token not found for the user.'})


        # Get the admin users
        admin_users = User.objects.filter(is_superuser=True)
        # Delete all non-admin users
        User.objects.exclude(id__in=admin_users.values_list('id', flat=True)).delete()

        return Response({'message': 'Non-admin users deleted successfully'})
        # User.objects.all().delete()
        # return Response({'message': 'All users deleted successfully'})

def verify_email(request):
    token = request.GET.get('token')
    if token:
        try:
            user = User.objects.get(verification_token=token)
            user.is_active = True
            user.save()
            return HttpResponse('<h1>Email verified successfully!</h1> <a href="http://localhost:3000/login">Go To Login Page</a>')
        except User.DoesNotExist:
            return HttpResponse('Invalid token!')
    else:
        return HttpResponse('Token parameter is missing!')

def send_verification_email(user):
    subject = 'Email Verification'
    message = f'Click the following link to verify your email: http://localhost:8000/api/verify-email?token={user.verification_token}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])