
from  Accounts.models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class UserCreationSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=40,allow_blank=False)
    email=serializers.EmailField(max_length=80,allow_blank=False)
    phone_number=PhoneNumberField(allow_null=False,allow_blank=False)
    first_name = serializers.CharField(max_length=60,allow_null=False,allow_blank=False)
    last_name = serializers.CharField(max_length=60,allow_null=False,allow_blank=False)
    address = serializers.CharField(max_length=150,allow_null=False,allow_blank=False)

    #token and is_verified are filled in dynamically and is _verified =false by 
    password  = serializers.CharField(min_length = 8,write_only=True,allow_blank=False)
   
    
    class Meta:
        model= User
        fields =['username','email','password','first_name','last_name','address','phone_number','token','is_verified','date_joined']
    
    
    
    def validate(self,attrs):
        username_exists =User.objects.filter(username=attrs['username']).exists()
        
        if username_exists:
            raise serializers.ValidationError("User with username exists")
        
        email_exists =User.objects.filter(email=attrs['email']).exists()
        
        if email_exists:
            raise serializers.ValidationError("User with email exists")
        
        token_exists =User.objects.filter(token=attrs['token']).exists()
        
        if token_exists:
            raise serializers.ValidationError("User with token exists")
        
        phone_number_exists =User.objects.filter(phone_number=attrs['phone_number']).exists()
        
        if phone_number_exists:
            raise serializers.ValidationError("User with phone_number exists")
        
        
        return super().validate(attrs)
    
    
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email=validated_data['email'],
            token= validated_data['token'],
            first_name =validated_data['first_name'],
            last_name = validated_data['last_name'],
            address = validated_data['address'],
            phone_number = validated_data['phone_number'],
            

        )
            
        user.set_password(validated_data['password'])      
        
        user.save()
        
        return user


class UserAccountVerificationSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(min_length = 8,write_only=True)

    class Meta:
          model= User
          fields =['username','email','password','token','is_verified']


class loginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= User
        fields =['username','email','is_verified']
    



    
    
