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
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from urllib.parse import urlencode, urljoin
from rudrakhashop import settings
from django.http import HttpResponse
import datetime
from django.db import transaction
import secrets

## import atomic


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password1 = request.data.get("password")
        password2 = request.data.get("confirmPassword")

        if not email or not password1 or not password2:
            return Response(
                data={"status": False, "message": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                data={"status": False, "message": "Email already registered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password1 != password2:
            return Response(
                data={
                    "status": False,
                    "message": "Password and confirm password do not match.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Create user with is_active=False
            first_name = first_name or ""
            last_name = last_name or ""
            customer = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
                is_active=False,
            )

            # Generate a secure verification token
            verification_token = secrets.token_urlsafe(64)

            # Save token to OTP model
            otp_obj = OTP.objects.create(user=customer, otp=verification_token)

            # Generate verification URL (backend URL)
            uid = urlsafe_base64_encode(force_bytes(customer.pk))
            # Use Django backend URL for verification
            verification_url = (
                f"{settings.BASE_URL}/account/verify-email/{uid}/{verification_token}/"
            )

            # Send verification email
            try:
                subject = "Verify your email"
                email_template = get_template("verification_email.html")
                email_content = email_template.render(
                    {
                        "user": customer,
                        "verification_url": verification_url,
                        "site_name": settings.SITE_NAME,
                        "expiry_hours": 24,  # Token expires in 24 hours
                    }
                )

                email_message = EmailMessage(
                    subject, email_content, settings.DEFAULT_FROM_EMAIL, [email]
                )
                email_message.content_subtype = "html"
                email_message.send()
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                # Still continue even if email fails

            # Create token for API authentication
            # token, _ = Token.objects.get_or_create(user=customer)

            return Response(
                data={
                    "status": True,
                    "message": "User registered successfully. Please verify your email by clicking the link we sent.",
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(e)
            return Response(
                data={"status": False, "message": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            # Decode user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            # Check if token exists and is valid
            try:
                # Get the latest token for the user
                token_obj = OTP.objects.filter(user=user).latest("created_at")

                # Check if token is expired (valid for 24 hours)
                time_difference = (
                    datetime.datetime.now(datetime.timezone.utc) - token_obj.created_at
                )
                if time_difference.total_seconds() > 86400:  # 24 hours
                    html_content = """
                    <html>
                    <head>
                        <title>Verification Failed</title>
                        <style>
                            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                            .container { max-width: 600px; margin: 0 auto; }
                            .error { color: #e74c3c; }
                            h1 { color: #3498db; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1 class="error">Verification Failed</h1>
                            <p>Your verification link has expired. Please request a new one.</p>
                        </div>
                    </body>
                    </html>
                    """
                    return HttpResponse(html_content, content_type="text/html")

                # Verify token
                if token_obj.otp != token:
                    html_content = """
                    <html>
                    <head>
                        <title>Verification Failed</title>
                        <style>
                            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                            .container { max-width: 600px; margin: 0 auto; }
                            .error { color: #e74c3c; }
                            h1 { color: #3498db; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1 class="error">Verification Failed</h1>
                            <p>Invalid verification link. Please make sure you are using the correct link.</p>
                        </div>
                    </body>
                    </html>
                    """
                    return HttpResponse(html_content, content_type="text/html")

                # Activate user
                user.is_active = True
                user.save()

                # Delete used token
                token_obj.delete()

                # Return success HTML page
                html_content = f"""
                <html>
                <head>
                    <title>Email Verified</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                        .container {{ max-width: 600px; margin: 0 auto; }}
                        .success {{ color: #2ecc71; }}
                        h1 {{ color: #3498db; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1 class="success">Email Verified Successfully!</h1>
                        <p>Your email has been verified and your account is now active.</p>
                        <p>You can now login to your account.</p>
                    </div>
                </body>
                </html>
                """
                return HttpResponse(html_content, content_type="text/html")

            except OTP.DoesNotExist:
                html_content = """
                <html>
                <head>
                    <title>Verification Failed</title>
                    <style>
                        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                        .container { max-width: 600px; margin: 0 auto; }
                        .error { color: #e74c3c; }
                        h1 { color: #3498db; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1 class="error">Verification Failed</h1>
                        <p>Invalid verification link. Please request a new verification email.</p>
                    </div>
                </body>
                </html>
                """
                return HttpResponse(html_content, content_type="text/html")

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            html_content = """
            <html>
            <head>
                <title>Verification Failed</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .container { max-width: 600px; margin: 0 auto; }
                    .error { color: #e74c3c; }
                    h1 { color: #3498db; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="error">Verification Failed</h1>
                    <p>Invalid verification link. Please make sure you are using the correct link.</p>
                </div>
            </body>
            </html>
            """
            return HttpResponse(html_content, content_type="text/html")
        except Exception as e:
            html_content = f"""
            <html>
            <head>
                <title>Verification Failed</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                    .container {{ max-width: 600px; margin: 0 auto; }}
                    .error {{ color: #e74c3c; }}
                    h1 {{ color: #3498db; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="error">Verification Failed</h1>
                    <p>An error occurred during verification. Please try again later.</p>
                </div>
            </body>
            </html>
            """
            return HttpResponse(html_content, content_type="text/html")


class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        if not email:
            return Response(
                data={"status": False, "message": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)

            if user.is_active:
                return Response(
                    data={
                        "status": False,
                        "message": "This email is already verified.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Delete any existing tokens for this user
            OTP.objects.filter(user=user).delete()

            # Generate a new verification token
            verification_token = secrets.token_urlsafe(64)

            # Save token to OTP model
            OTP.objects.create(user=user, otp=verification_token)

            # Generate verification URL (backend URL)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f"{settings.BASE_URL}/api/account/verify-email/{uid}/{verification_token}/"

            # Send verification email
            try:
                subject = "Verify your email"
                email_template = get_template("verification_email.html")
                email_content = email_template.render(
                    {
                        "user": user,
                        "verification_url": verification_url,
                        "site_name": settings.SITE_NAME,
                        "expiry_hours": 24,
                    }
                )

                email_message = EmailMessage(
                    subject, email_content, settings.DEFAULT_FROM_EMAIL, [email]
                )
                email_message.content_subtype = "html"
                email_message.send()
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                return Response(
                    data={"status": False, "message": f"Error sending email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                data={
                    "status": True,
                    "message": "Verification email sent successfully.",
                },
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                data={"status": False, "message": "No user found with this email."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data={"status": False, "message": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Update LoginView to check for email verification
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            username = request.data.get("username")
            password = request.data.get("password")

            if not (email or username):
                return Response(
                    {
                        "status code": status.HTTP_400_BAD_REQUEST,
                        "message": "Email or username is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = None
            if email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return Response(
                        {
                            "status code": status.HTTP_400_BAD_REQUEST,
                            "message": "Invalid email",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return Response(
                        {
                            "status code": status.HTTP_400_BAD_REQUEST,
                            "message": "Invalid username",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            if not check_password(password, user.password):
                return Response(
                    {
                        "status code": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid password",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if user is active (verified email)
            if not user.is_active:
                # Generate new verification link
                verification_token = secrets.token_urlsafe(64)
                OTP.objects.filter(user=user).delete()
                OTP.objects.create(user=user, otp=verification_token)

                # Generate verification URL
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verification_url = f"{settings.BASE_URL}/account/verify-email/{uid}/{verification_token}/"

                try:
                    subject = "Verify your email"
                    email_template = get_template("verification_email.html")
                    email_content = email_template.render(
                        {
                            "user": user,
                            "verification_url": verification_url,
                            "site_name": settings.SITE_NAME,
                            "expiry_hours": 24,
                        }
                    )

                    email_message = EmailMessage(
                        subject,
                        email_content,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                    )
                    email_message.content_subtype = "html"
                    email_message.send()
                except Exception as e:
                    print(f"Error sending email: {str(e)}")

                return Response(
                    {
                        "status code": status.HTTP_403_FORBIDDEN,
                        "message": "Email not verified. A new verification link has been sent to your email.",
                        "verified": False,
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            token, _ = Token.objects.get_or_create(user=user)

            response = {
                "status code": status.HTTP_200_OK,
                "message": "User login successful",
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "token": token.key,
                "verified": True,
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            return Response(
                {
                    "status code": status.HTTP_400_BAD_REQUEST,
                    "message": "An error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            print("this is working")
            print(request.user)
            request.user.auth_token.delete()
            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            old_password = serializer.data.get("old_password")
            if not user.check_password(old_password):
                response = {
                    "status": False,
                    "status code": status.HTTP_400_BAD_REQUEST,
                    "message": "Old password is incorrect.",
                }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)

            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")

            if new_password != confirm_new_password:
                response = {
                    "status": False,
                    "status code": status.HTTP_400_BAD_REQUEST,
                    "message": "New passwords do not match.",
                }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)

            user.set_password(new_password)
            user.save()
            response = {
                "status": True,
                "status code": status.HTTP_200_OK,
                "message": "Password updated successfully.",
            }
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)
        response = {
            "status": False,
            "status code": status.HTTP_400_BAD_REQUEST,
            "message": serializer.errors,
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
