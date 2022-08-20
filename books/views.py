from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import viewsets,filters
from .serializers import BookSerializers
# from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .models import Book
# Create your views here.

@extend_schema(
        request=BookSerializers,
        responses={201: BookSerializers},
    )
class BooksViewSets(viewsets.ModelViewSet):
  queryset = Book.objects.all().order_by("-date_created")
  serializer_class = BookSerializers
  filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
  search_fields = ['book_category','author','title']
 

 
