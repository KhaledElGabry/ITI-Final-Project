from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from account.views import CustomLogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', CustomLogoutView.as_view(), name='admin_logout'),
    path('api/', include('account.urls')),
    path('api/product/', include('product.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/order/',include('order.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
