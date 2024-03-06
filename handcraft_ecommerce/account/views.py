from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt
import datetime
from rest_framework import status
from .app import upload_photo,delete_photos
import os
from urllib.parse import unquote

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .tokens import account_activation_token  # You need to create this token generator
from django.core.mail import EmailMessage

from django.utils.http import urlsafe_base64_decode


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(request.data['first_name'])
        # print(request.data['image'])

        user = serializer.save()

        # Send verification email
        self.send_verification_email(request, user)

        return Response({"message": "success"})

    def send_verification_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        # domain = request.get_host()  # Get the domain from the request
        domain = "localhost:3000"
        verification_link = f'http://{domain}/activate/?uid={urlsafe_base64_encode(force_bytes(user.pk))}&token={account_activation_token.make_token(user)}'
        message = f'Hello {user.username},\n\nPlease click on the following link to activate your account:\n{verification_link}'
        email = EmailMessage(
            subject=subject,
            body=message,
            to=[user.email],
        )
        email.send()


class ActivateAccount(APIView):
    def get(self, request):
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')
        
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)


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

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), # expiration 1 day
            'iat': datetime.datetime.utcnow() # tokenCreatedAt
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        # response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "message":"success",
            "token": token,  # Decode here if needed
            "user": UserSerializer(user).data
        }
        return response
    
class UserView(APIView):
    # delete user
    def delete(self, request, id):
        try:
            user = User.userDelete(id)
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # update user
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
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
        return Response({'Users':dataJSON})
    
    

    def get(self, request):
        users = User.usersList()
        dataJSON = UserSerializer(users, many=True).data
        return Response({'Users': dataJSON})
    
    def delete(self, request):
        print("User.objects.all().delete():  ",User.objects.all().delete())
        User.objects.all().delete()
        return Response({'message': 'All users deleted successfully'})

