from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics, parsers, permissions, status, views, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from account import serializers
from account.models import *
from account.serializers import *
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_str
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from urllib.parse import urlencode, urljoin
from rudrakhashop import settings

# from .serializers import AddressSerializer

# class AddressViewSet(viewsets.ModelViewSet):
#     serializer_class = AddressSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Addresses.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password1 = request.data.get("password")
        password2 = request.data.get("confirmPassword")
       
        
        if not email or not password1 or not password2:
            return Response(
                data={"status": False, "message": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                data={"status": False, "message": "Email already registered."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if password1 != password2:
            return Response(
                data={"status": False, "message": "Password and confirm password do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            print('reaching here')
            first_name = first_name or ""
            last_name = last_name or ""
            customer = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password1)
            print('reaching here')
            
            token, _ = Token.objects.get_or_create(user=customer)
            print(token)
            return Response(
                data={"status": True, "message": "User registered successfully.", "token": token.key},
                status=status.HTTP_201_CREATED 
            )
        
        except Exception as e:
            print(e)
            return Response(
                data={"status": False, "message": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            
            email = request.data.get('email')
            username = request.data.get('username')
            password = request.data.get('password')

            
            if not (email or username):
                return Response({
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Email or username is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            
            user = None
            if email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return Response({
                        'status code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid email'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return Response({
                        'status code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid username'
                    }, status=status.HTTP_400_BAD_REQUEST)

            
            if not check_password(password, user.password):
                return Response({
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid password'
                }, status=status.HTTP_400_BAD_REQUEST)

            
            token, _ = Token.objects.get_or_create(user=user)

            
            response = {
                'status code': status.HTTP_200_OK,
                'message': 'User login successful',
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': token.key
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            return Response({
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'An error occurred',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = LoginSerializer
    def post(self, request,  *args, **kwargs):
        try:
            print('this is working') 
            print(request.user)
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            old_password = serializer.data.get('old_password')
            if not user.check_password(old_password):
                response = {
                    'status' : False,
                    'status code' : status.HTTP_400_BAD_REQUEST,
                    'message': 'Old password is incorrect.',
                    }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)

            new_password = serializer.data.get('new_password')
            confirm_new_password = serializer.data.get('confirm_new_password')

            if new_password != confirm_new_password:
                response = {
                    'status' : False,
                    'status code' : status.HTTP_400_BAD_REQUEST,
                    'message': 'New passwords do not match.',
                    }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)

            user.set_password(new_password)
            user.save()
            response = {
                'status' : True,
                'status code' : status.HTTP_200_OK,
                'message': "Password updated successfully.",
                }
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)
        response = {
            'status' : False,
            'status code' : status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors,
            }
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)




 
class UserProfileDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user 



class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser]

    def get_object(self):
        return self.request.user
    

