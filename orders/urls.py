from django.urls import path, include

from rest_framework import routers
from .views import AllOrderViewSets


app_name = "orders"
router = routers.DefaultRouter()

router.register("", viewset=AllOrderViewSets)

urlpatterns = [path("", include(router.urls))]
