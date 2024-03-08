from django.urls import path
from .views import *

urlpatterns = [
        path('register/', RegisterView.as_view()),
        path('login/', LoginView.as_view()),
        # path('user/', UserView.as_view()),
        path('logout/', LogoutView.as_view()),
        path('allUser/', allUsers.as_view()),
        # delete & update based on method type delete/put
        path('profile/', UserView.as_view()),
        path('verify-email/', verify_email, name='verify_email')
]
