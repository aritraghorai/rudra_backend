from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileByPageNameView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, page_name):
        print(page_name)
        profile = get_object_or_404(Profile, page_name=page_name)
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
