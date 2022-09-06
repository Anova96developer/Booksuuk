
from itertools import product
from unittest import result
from rest_framework import serializers

from orders.models import Order
from account.models import User
from books.models import Book



class AllOrdersSerializer(serializers.ModelSerializer):
  
  
  username = serializers.StringRelatedField(source = 'user.username')
  book_category = serializers.StringRelatedField(source ='book.book_category')
  book_title = serializers.StringRelatedField(source ='book.title' )
  price_wrt_quantity = serializers.SerializerMethodField(method_name= 'get_price_wrt_quantity')

  class Meta :
    model = Order
    fields = ["username","order_Id","book_title","book_category","quantity","price_wrt_quantity","order_status","date_created","date_modified"]

    read_only_fields = ["order_Id","book_category","book_title","price_wrt_quantity"]


  
  def get_price_wrt_quantity (self,obj):
  
   result = obj.quantity * obj.book.price
  
  #worked , but not updated on the database

   return result




    



