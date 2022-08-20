from pyexpat import model
from attr import field, fields
from rest_framework import serializers

from books.models import Book

class BookSerializers(serializers.ModelSerializer):

  class Meta:
    model = Book
    fields = "__all__"
    ordering = ["-date_created"]
    order_by =  ["date_created","date_modified"] 
     