


from distutils.log import Log
import email
from multiprocessing import context
from urllib import request
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .import serializers
import secrets
from django.core.mail import send_mail # for email
from django.conf import settings
from django.shortcuts import render,get_object_or_404
from .serializers import UserAccountVerificationSerializer, UserCreationSerializer,loginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
# from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
User=get_user_model()


# Create your views here.

class AllUsers(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializer
    
   
    @extend_schema(
        request= UserCreationSerializer,
        responses={201: UserCreationSerializer},
    )
    def get(self,request):

          users = User.objects.all()
          serializer = self.serializer_class(instance=users,many=True)
        
          return Response(data=serializer.data,status= status.HTTP_201_CREATED  )
        
       


class UserCreateView(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializer
    
    @extend_schema(
        request= UserCreationSerializer,
        responses={201: UserCreationSerializer},
    )
    def post(self,request):

        


        data = request.data
        
     
        serializer  = self.serializer_class(data=data)
        
        username = data['username']
        reciever_email = data['email']


         
        
        if serializer.is_valid():

            serializer.save()

            token =serializer.data['token']

            body  = f'Hi {username},\n You are seeing this message because you registered for Ebookify . Copy the code code below to verify your account   \n {token}'  

            send_mail(
           'Confirmation code for account verification',
            body,
            'Ebookify.app.com',
            [reciever_email],
              fail_silently=False,
            )

            return Response(data=serializer.data,status= status.HTTP_201_CREATED  )
        
        return  Response(data=serializer._errors,status=  status.HTTP_400_BAD_REQUEST)

class AccountVerificationView(generics.GenericAPIView):  
    serializer_class= UserAccountVerificationSerializer
    
    @extend_schema(
        request= UserAccountVerificationSerializer,
        responses={201: UserAccountVerificationSerializer},
    )
    def  put (self,request):
        user  = get_object_or_404(User,email = request.data['email'])
       
        # print(user.token) 
        if (user.token == request.data['token']):
     
             user.is_verified =   True
             user.save()

             serializer = self.serializer_class(instance=user)
             return  Response(data=serializer.data,status=status.HTTP_200_OK)

        return  Response(data={'message':'verification failed'},status=  status.HTTP_400_BAD_REQUEST)




class loginView(generics.GenericAPIView):
    serializer_class = loginSerializer


    def get_tokens_for_user(user):
     refresh = RefreshToken.for_user(user)

     return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    @extend_schema(
        request= loginSerializer,
        responses={201: loginSerializer},
    )
    def post (self,request):
          user  = get_object_or_404(User,email = request.data['email'])
         
         #Todo compare passwor , and compare verify

          passwordFlag = user.check_password(request.data['password'])

          if passwordFlag:
               
             if (user.is_verified ):

              print('True')
              tokens = loginView.get_tokens_for_user(user=user)
              serializer = self.serializer_class(instance=user)
              return  Response(data={'message':serializer.data,'token':tokens},status=status.HTTP_200_OK)

             return  Response(data={'message':'Account not activated'},status=  status.HTTP_400_BAD_REQUEST)     
        

          return  Response(data={'message':'Authentication Failed'},status=  status.HTTP_401_UNAUTHORIZED)   



        
             

