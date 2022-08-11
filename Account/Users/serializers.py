from multiprocessing import AuthenticationError
from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


User=get_user_model()
class UserSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True,write_only=True)
    email=serializers.EmailField()
    def validate(self, attrs):
        SignUp_as=attrs.get('SignUp_as')
        if SignUp_as == 'F':
            
            genre=serializers.HiddenField(default='F',read_only=True)
            return genre
        
        return super().validate(attrs)
    class Meta:
        model=User
        fields=['SignUp_as','full_name','email','create_on','password','confirm_password']
        
        extra_kwargs = {
            'password': {'write_only':True},
            'confirm_password':{'write_only':True}
         }
    
    def validate(self, data):
        email = data.get('email', None)
        if email:
            data['Username'] = email
        return data
        
    def validate_email(self,email):
        existing_email=User.objects.filter(email=email).first()
        if existing_email:
            raise serializers.ValidationError("this Email is already exist!!")
        return email