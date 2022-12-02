from django.urls import path, include

from rest_framework import routers
from .views import BooksViewSets


app_name = "books"
router = routers.DefaultRouter()

router.register("", viewset=BooksViewSets)

urlpatterns = [path("", include(router.urls))]
