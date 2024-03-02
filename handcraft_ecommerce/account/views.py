from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from rest_framework import status


from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .tokens import account_activation_token  # You need to create this token generator
from django.core.mail import EmailMessage
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
        domain = request.get_host()  # Get the domain from the request
        verification_link = f'http://{domain}/activate/?uid={urlsafe_base64_encode(force_bytes(user.pk))}&token={account_activation_token.make_token(user)}'
        message = f'Hello {user.username},\n\nPlease click on the following link to activate your account:\n{verification_link}'
        email = EmailMessage(
            subject=subject,
            body=message,
            to=[user.email],
        )
        email.send()

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

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data Updated Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserView(APIView):

#     def get(self, request):
#         token = request.COOKIES.get('jwt')

#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')

#         user = User.objects.filter(id=payload['id']).first()
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

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
    
    
