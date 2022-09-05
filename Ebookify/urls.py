

from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# for images upload
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView






urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('api/v1/users/',include('account.urls')),
    path('api/v1/books/', include('books.urls')),
    path('api/v1/orders/', include('orders.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Optional UI:
    path('api/v1/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
