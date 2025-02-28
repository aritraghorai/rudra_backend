from django.urls import re_path, include, path
from account import views
from rest_framework.routers import DefaultRouter
# from .views import AddressViewSet

# router = DefaultRouter()
# router.register('addresses', AddressViewSet, basename='address')

# app_name = 'accouts'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileDetailsView.as_view(), name='profile'),
    path('profile-update/', views.UserProfileUpdateView.as_view(), name='profile-update'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    # path('', include(router.urls)),
]

