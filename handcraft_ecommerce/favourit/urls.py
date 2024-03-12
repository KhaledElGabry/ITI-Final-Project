from django.urls import path
from . import views

urlpatterns = [
    path('remove-from-favorite/<int:id>/', views.remove_from_Favorite, name='remove_from_favorite'),
    path('add-to-favorite/<int:id>/', views.add_to_Favorite, name='add_to_favorite'),
    path('user-favorite/', views.user_favorite, name='user_favorite'),
]
