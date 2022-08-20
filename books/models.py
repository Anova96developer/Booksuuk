from email.policy import default
from pyexpat import model
from random import choices
from secrets import choice
from django.db import models
import uuid

from django.forms import CharField


class Book  (models.Model):
   BOOK_CATEGORY = (
           ('ROMANCE','romance'),
           ('FICTION','fiction'),
           ('DRAMA','drama'),
           ('POLITICS','politics'),
           ('CRIME','crime'),
          
             )

   book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   title =  models.CharField(max_length=225,null = False, blank= False)
   book_category = models.CharField(max_length=50,null =False,choices = BOOK_CATEGORY,default = BOOK_CATEGORY[0][0])
   author = models.CharField(max_length=201,null = False, blank= False)
   description = models.CharField(max_length=500,null = False, blank= False)
   price= models.DecimalField(max_digits=10, decimal_places=2)
   book_image=models.ImageField(upload_to = 'book-images/',default ='book-images/84279_1646620000.webp', null=False)
   isbn = models.CharField(max_length=100,blank=False,null = False)
   date_created =  models.DateTimeField(auto_now=True)
   date_modified = models.DateTimeField(auto_now_add=True)


   def __str__(self):
        return self.title





              




