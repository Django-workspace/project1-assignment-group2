from xml.dom import ValidationErr
from rest_framework.decorators import APIView
from rest_framework import mixins,generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser 
from .serializers import *
from .models import *
from .permissions import *
import jwt,datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse



# Create your views here.


        
class SignUp(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all() 
    
    # def get (self,request):
    #     # permission_classes=[IsAuthenticated]
    #     # permission_classes=[IsAdminUser]
    #     user=User.objects.all()
    #     serializer=self.serializer_class(instance=user,many=True)
    #     return Response(data=serializer.data,status=status.HTTP_200_OK)
     
    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class Login(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class=UserSerializerLogIn
    def post (self,request):  
        email=request.data['email']
        password=request.data['password']
        
        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user is not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('password is incorrect')
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow()  
        }
        
        token=jwt.encode(payload,'secret', algorithm='HS256')
        response=Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data={
                'jwt':token
            }
        # Status=status.HTTP_202_ACCEPTED
        return response#,Status
       

   
class UserView(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    def get(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthentacated')
        
        
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    
    
class LogOut(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'user has been logout successful!!' 
        }
        
        return response,status.HTTP_202_ACCEPTED
    

    
# class ResetPassword(generics.GenericAPIView):
#     serializer_class=ResetPassordSerializer
#     def post(self,request):
#         serializer=self.serializer_class(data=request.data)
#         email=request.data['email']
        
#         if User.objects.filter(email=email).exists():
            
#             user=User.objects.get(email=email)
#             uidb64=urlsafe_base64_encode(smart_bytes(user.id))
#             token=PasswordResetTokenGenerator().make_token(user)
#             current_site= get_current_site(request=request).domain
#             relativeLink= reverse('passwordReset-confirm',kwargs={'uidb64':uidb64,'token':token})
#             absurl = 'http://'+ current_site+ relativeLink
#             email_body='Hello, \n Use link bellow to Reset your password \n'+absurl
#             data={
#                 'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
#             Util.send_email (data)
#             return Response({'Success':'we have send you  a email for reset password'}, status=status.HTTP_200_OK)
#         return Response({'Not found',status.HTTP_400_BAD_REQUEST})
    
class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get (self, request, uidb64,token):
        
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'errow': 'this link is Invalid, Please request a new one'},status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success':True,'message':'Credentials valid','uidb64':uidb64,'token':token},status.HTTP_200_OK)
           
        except DjangoUnicodeDecodeError as indentifier:
             if not PasswordResetTokenGenerator().check_token(user):
                return Response({'errow': 'this link is Invalid, Please request a new one'},status=status.HTTP_401_UNAUTHORIZED)
            
            
class SetNewPasswordAPI(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class=SetNewPasswordserializer
    def put(self,request):
        serializer=self.serializer_class(data=request)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Reset Password successfull'},status=status.HTTP_200_OK)
