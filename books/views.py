from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from httplib2 import Response
from rest_framework import viewsets,filters
from rest_framework.response import Response
from .serializers import BookSerializers
# from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.permissions import IsAuthenticated
from .models import Book
# Create your views here.


class BooksViewSets(viewsets.ModelViewSet):
  queryset = Book.objects.all().order_by("-date_created")
  serializer_class = BookSerializers
  permission_classes = [IsAuthenticated]
  filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
  search_fields = ['book_category','author','title']


  def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

 

 
