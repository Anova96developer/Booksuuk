
from  Accounts.models import User
from rest_framework import serializers


class UserCreationSerializer(serializers.ModelSerializer):
    username =serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    password  = serializers.CharField(min_length = 8,write_only=True)
    is_verified = serializers.BooleanField(default = False)
    
    class Meta:
        model= User
        fields =['username','email','password','token','is_verified']
    
    
    
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
        
        
        return super().validate(attrs)
    
    
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email=validated_data['email'],
            token= validated_data['token'],
           

        )
            
        user.set_password(validated_data['password'])      
        
        user.save()
        
        return user


# class UserAccountVerificationSerializer(serializers.ModelSerializer)