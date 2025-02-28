from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.models import update_last_login
from django.db.models import Q
from django.utils import timezone
from .models import *

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=False)
    username=serializers.CharField(max_length=200, required=False)
    password = serializers.CharField(max_length=128, write_only=True)
   
    def validate(self, data):
        email = data.get("email", None)
        username=data.get('username', None)
        password = data.get("password", None)
        if email:
            if not User.objects.filter(email=email, is_active=True, is_email=True ).exists():
                raise serializers.ValidationError(
                    'A user with this email and password is not found.'
                )
            user = authenticate(email=email, password=password)
        elif username:
            if not User.objects.filter(username=username, is_active=True).exists():
                raise serializers.ValidationError(
                    'A user with this email and password is not found.'
                )
            user = authenticate(username=username, password=password)

        if user is None:

            raise serializers.ValidationError (
            "A user with this email and password is not found."
            
            )
        try:
            return {
                "user_email":user.email,
            }

        except user.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email/Phone and password does not exists", 
            )
def authenticate(username=None, email=None,password=None, **kwargs):
    try:
        if email:
            try:
                user=User.objects.get(email = email)
            except Exception as e:
                pass
        elif username:
            try:
                user=User.objects.get(username = username)
            except Exception as e:
                pass
       
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


  
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name", "last_name", "email", "profile_pic",  'phone', 'birth_day', 'gender','accepts_marketing']   


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name", "last_name", "profile_pic", 'phone','birth_day', 'gender','accepts_marketing']
        

    def validate_birth_day(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value

    def validate_gender(self, value):
        valid_genders = ["Male", "Female", "Other"]
        if value and value not in valid_genders:
            raise serializers.ValidationError(f"Gender must be one of {valid_genders}.")
        return value
    
    
# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Addresses
#         fields = ['id', 'user', 'first_name', 'last_name', 'company', 
#                  'address', 'apartment', 'city', 'country', 'zipcode', 'phone']
#         read_only_fields = ['user']