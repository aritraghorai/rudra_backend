from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import FAQ, Product, ProductVariant, ProductCategory
from .serializers import FAQSerializer, ProductCategorySerializer, ProductSerializer, ProductVariantSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# Create your views here.


class ProductsListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        products = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FAQListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request,pk):
        try:
            category = ProductCategory.objects.get(id=pk)
        except ProductCategory.DoesNotExist:
            return Response({'message':'Category Not Found'},status=status.HTTP_400_BAD_REQUEST)
        faq = FAQ.objects.filter(category=category)
        serializer = FAQSerializer(faq, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

