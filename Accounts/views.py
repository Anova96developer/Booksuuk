

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .import serializers
import secrets
from django.core.mail import send_mail # for email

# Create your views here.

class HelloAuthView(generics.GenericAPIView):
        
   
    def get(self,request):
        return Response(data={"message":"Hello Auth"},status=status.HTTP_200_OK)

class UserCreateView(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializer
    
    
    def post(self,request):

        token = secrets.token_hex(30)

        request.data.update({'token':token})

        data = request.data
         
        
        
        serializer  = self.serializer_class(data=data)
        
        username = data['username']
        reciever_email = data['email']


        body  = f'Hi {username},\n You are seeing this message because you registered for Ebookify . Copy the code code below to verify your account   \n {token}'   

        if serializer.is_valid():
            serializer.save()


            send_mail(
           'Confirmation code for account verification',
            body,
            'Ebookify.app.com',
            [reciever_email],
              fail_silently=False,
            )

            return Response(data=serializer.data,status= status.HTTP_201_CREATED  )
        
        return  Response(data=serializer._errors,status=  status.HTTP_400_BAD_REQUEST)