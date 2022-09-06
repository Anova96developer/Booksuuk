from multiprocessing import context
from tkinter import Entry
import uuid
from django import views
from django.shortcuts import render
from requests import request
from rest_framework import viewsets,filters,status
from rest_framework.response import Response


from django.shortcuts import render,get_object_or_404
from yaml import BlockMappingStartToken, serialize
from account import serializers
from account.models import User

from books.models import Book
from orders.serializers import AllOrdersSerializer
from .models import Order
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action




class OrderViewSets(viewsets.ModelViewSet):

  queryset = Order.objects.all().order_by("-date_created")
  serializer_class = AllOrdersSerializer
  permission_classes = [AllowAny]
  http_method_names = ["get","post","put","patch","delete"]
  #change the permision later
  filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
 
  search_fields = ["order_Id","book__book_category","book__title","user__username","order_status"]
  ordering_fields = ["created_at"]
 

  def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




 
#   def list (self,request,*args, **kwargs): 
#      queryset = Order.objects.all().order_by("-date_created")   
#      serializer  = self.serializer_class(queryset,many =True)
#      return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

#   @action(
#     methods=['GET'],
#     detail=False,
#     serializer_class= AllOrdersSerializer,
#     url_path='customer-order/<pk:user>',
#     url_name='customer_order'


#   )   
#   def customer_order(self,request,*args, **kwargs):
#     user:uuid = request.GET.get['user']
#     queryset = Order.objects.filter(pk=user).first()
#     serializer  = self.serializer_class(queryset,many =True)
#     return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)









  
















  





  




