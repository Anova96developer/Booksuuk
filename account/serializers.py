
import email
import secrets
from  account.models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class UserCreationSerializer(serializers.ModelSerializer):

    username=serializers.CharField(max_length=40,allow_blank=False)
    email=serializers.EmailField(max_length=80,allow_blank=False)
    phone_number=PhoneNumberField(allow_null=False,allow_blank=False)
    first_name = serializers.CharField(max_length=60,allow_null=False,allow_blank=False)
    last_name = serializers.CharField(max_length=60,allow_null=False,allow_blank=False)
    address = serializers.CharField(max_length=150,allow_null=False,allow_blank=False)

    password  = serializers.CharField(min_length = 8,write_only=True,allow_blank=False)
   
    
    class Meta:
        model= User
        fields =['id','username','email','password','first_name','last_name','address','phone_number','token','is_verified','date_joined']
        read_only_fields= ['id','is_verified','date_joined','token',]


    
    
    
    def validate(self,attrs):
        username_exists =User.objects.filter(username=attrs['username']).exists()
        
        if username_exists:
            raise serializers.ValidationError("User with username exists")
        
        email_exists =User.objects.filter(email=attrs['email']).exists()
        
        if email_exists:
            raise serializers.ValidationError("User with email exists")
        
       
        
        phone_number_exists =User.objects.filter(phone_number=attrs['phone_number']).exists()
        
        if phone_number_exists:
            raise serializers.ValidationError("User with phone_number exists")
        
        
        return super().validate(attrs)
    
    
    
    def create(self, validated_data):

        password = validated_data.pop('password')
        token = secrets.token_hex(30)

        validated_data['token'] = token

        user =  super().create(validated_data)



        user.set_password(password)  
    
        
        user.save()
        
        return user


class UserAccountVerificationSerializer(serializers.ModelSerializer):
    

    class Meta:
          model= User
          fields =['username','email','token','is_verified']
          read_only_fields = ['username','is_verified']



class loginSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(min_length = 8,write_only=True)
    class Meta:
        model= User
        fields =['username','email','password','is_verified']
        read_only_fields = ['is_verified','username']

    



    
    
