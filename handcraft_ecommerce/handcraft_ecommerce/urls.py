from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('theme/', include("theme.urls")),
    path('api/', include('account.urls')),
]
