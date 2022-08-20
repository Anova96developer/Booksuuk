from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializers
from drf_yasg.utils import swagger_auto_schema

from .models import Book
# Create your views here.

@swagger_auto_schema()
class BooksViewSets(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializers
