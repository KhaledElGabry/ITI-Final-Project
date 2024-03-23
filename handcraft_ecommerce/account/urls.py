from django.urls import path, include
from .views import *
from django.contrib.auth import views

urlpatterns = [
        path('register/', RegisterView.as_view()),
        path('login/', LoginView.as_view()),
        # path('user/', UserView.as_view()),
        path('logout/', LogoutView.as_view()),
        path('allUser/', allUsers.as_view()),
        # delete & update based on method type delete/put
        path('profile/', UserView.as_view()),
        path('verify-email/', verify_email, name='verify_email'),
        # Password reset flow
        path('changePassword/', ChangePasswordView.as_view(), name='change_password'),
        path('Forgot-Password/', ForgotPasswordView.as_view(), name='forgot-password'),
        path('verifyResetCode/', VerifyResetCodeAPI.as_view(), name='verifyResetCode'),
        path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
]
