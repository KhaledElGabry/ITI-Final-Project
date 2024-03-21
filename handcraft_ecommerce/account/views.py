from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .serializers import UserSerializer, ChangePasswordSerializer
from .models import User
from .models import CustomToken
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import jwt
from datetime import timedelta
from django.utils import timezone  
from rest_framework import status, generics
from .app import upload_photo, delete_photos
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
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
import secrets
import string
from django.contrib.auth import get_user_model



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
            media_file = os.path.join(os.getcwd(), user.image.path)
            if os.path.isfile(media_file):
                os.remove(media_file)
                print(f"Deleted: {media_file}")
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
            media_file = os.path.join(os.getcwd(), user.image.path)
            if os.path.isfile(media_file):
                os.remove(media_file)
                print(f"Deleted: {media_file}")
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response({'message': 'Data Updated Successfully', "user":serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            token = CustomToken.objects.get(user=request.user.id)
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
            return HttpResponse("""
                            <html>
                            <head>
                                <title>Email Verified</title>
                            </head>
                            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; padding: 20px;">
                                <div style="font-size: 48px; color: #28a745; margin-bottom: 20px;">&#10004;</div>
                                <h1 style="color: #333;">Email verified successfully!</h1>
                                <p> <a href="http://localhost:3000/login" style="display: inline-block; padding: 10px 20px; background-color: black; color: #fff; text-decoration: none; border-radius: 5px;">Login</a>.</p>
                            </body>
                            </html>
                        """)
        except User.DoesNotExist:
            return HttpResponse('Invalid token!')
    else:
        return HttpResponse('Token parameter is missing!')

def send_verification_email(user):
    subject = 'Email Verification'
    message = f'Click the following link to verify your email: http://localhost:8000/api/verify-email?token={user.verification_token}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    



from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            self.logout(request)
            return HttpResponseRedirect(self.get_next_page())
        else:
            return super().dispatch(request, *args, **kwargs)
        

class ChangePasswordView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
 
    serializer_class= ChangePasswordSerializer
    model = User
        
    def patch(self, request, *args, **kwargs):

        try:
            user = User.objects.get(id=request.user.id)
            # Check if the user's token has expired
            token = CustomToken.objects.get(user=request.user)
            if token.expires and token.is_expired():
                raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
            
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except CustomToken.DoesNotExist:
            return Response({'error': 'User must login first'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)})

        
        self.object=request.user
        serializer = self.get_serializer(data = request.data)
        
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old password" : ["wornd password"]}, status = status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response({"message": "password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)
    
    
    
    
# Forgot Password API

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data['email']

        try:
            user = get_user_model().objects.get(email=email)

            def create_and_store_random_code(user, code_length=6, timeout_minutes=3):
                random_code = ''.join(secrets.choice(string.digits) for _ in range(code_length))
                user.random_code = random_code
                user.random_code_expires = timezone.now() + timedelta(minutes=timeout_minutes)
                user.save()
                return random_code

            random_code = create_and_store_random_code(user)

            subject = 'Password Reset'
            message = f'Your password reset code is: {random_code}\nThis code will expire in 3 minutes.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            return Response({'message': 'Password reset code sent to your email'})

        except User.DoesNotExist:
            return Response({'error': 'Email address may not be correct'}, status=status.HTTP_404_NOT_FOUND)




# Verify Reset Code API


class VerifyResetCodeAPI(APIView):
    def post(self, request):
        resetCode = request.data['resetCode'] 

        try:
            user = get_user_model().objects.filter(random_code=resetCode).first()
            if not user or user.random_code_expires < timezone.now():
                return Response({'error': 'Invalid or expired verification code'}, status=status.HTTP_400_BAD_REQUEST)


            user.random_code = None
            user.random_code_expires = None
            user.save()
            return Response({'message': 'Code verified successfully!'})

        except User.DoesNotExist:
            return Response({'error': 'Invalid or expired verification code'}, status=status.HTTP_400_BAD_REQUEST) # same error message for security reason

      

# Password Reset API

class PasswordResetView(APIView):
    def put(self, request):
        try:
            email = request.data['email']
            newPassword = request.data['newPassword']
            
            
            user = get_user_model().objects.get(email=email)

            try:
                validate_password(newPassword)
            except ValidationError as e:
                return Response({'error': ', '.join(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

            user.random_code = None
            user.random_code_expires = None
            user.set_password(newPassword)
            user.save()

            return Response({'message': f'Password reset successfully for user: {user.email}'})

        except User.DoesNotExist:
            return Response({'error': 'Email address may not be correct'}, status=status.HTTP_404_NOT_FOUND)

     

