from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('theme/', include("theme.urls")),
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
]
