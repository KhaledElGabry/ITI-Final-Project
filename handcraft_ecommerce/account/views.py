from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt
import datetime
from rest_framework import status

<<<<<<< HEAD

=======
>>>>>>> f6f70e3b156bee6e865922c276a4af8b2efd4565
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .tokens import account_activation_token  # You need to create this token generator
from django.core.mail import EmailMessage
<<<<<<< HEAD
=======
from django.utils.http import urlsafe_base64_decode

>>>>>>> f6f70e3b156bee6e865922c276a4af8b2efd4565
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email
        self.send_verification_email(request, user)

        return Response({"message": "success"})

    def send_verification_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
<<<<<<< HEAD
        domain = request.get_host()  # Get the domain from the request
=======
        # domain = request.get_host()  # Get the domain from the request
        domain = "localhost:3000"
>>>>>>> f6f70e3b156bee6e865922c276a4af8b2efd4565
        verification_link = f'http://{domain}/activate/?uid={urlsafe_base64_encode(force_bytes(user.pk))}&token={account_activation_token.make_token(user)}'
        message = f'Hello {user.username},\n\nPlease click on the following link to activate your account:\n{verification_link}'
        email = EmailMessage(
            subject=subject,
            body=message,
            to=[user.email],
        )
        email.send()
<<<<<<< HEAD
=======

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
>>>>>>> f6f70e3b156bee6e865922c276a4af8b2efd4565

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
<<<<<<< HEAD
    def get(self,request):
        users=User.usersList()
        dataJSON=UserSerializer(users,many=True).data
        return Response({'Users':dataJSON})
    
    
=======
    def get(self, request):
        users = User.usersList()
        dataJSON = UserSerializer(users, many=True).data
        return Response({'Users': dataJSON})
>>>>>>> f6f70e3b156bee6e865922c276a4af8b2efd4565
