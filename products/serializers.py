from rest_framework import serializers
from .models import (
    FAQ, ProductCategory, ProductSubCategory, ProductDesign, ProductSize, 
    Product, ProductVariant, ProductDesignAssociation, ProductImage
)

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'image', 'descriptions']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category','image']

class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubCategory
        fields = ['id', 'category', 'subcategory_name', 'image', 'description']

class ProductDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDesign
        fields = ['id', 'design_name', 'design_image', 'design_icon', 'design_description', 'design_price']


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['id', 'size_name']

class ProductVariantSerializer(serializers.ModelSerializer):
    size = ProductSizeSerializer()
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'size', 'price', 'stock']
        

class ProductDesignAssociationSerializer(serializers.ModelSerializer):
    design = ProductDesignSerializer()
    class Meta:
        model = ProductDesignAssociation
        fields = ['id', 'product', 'design']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    images = ProductImageSerializer(many=True)
    product_category = ProductCategorySerializer()
    product_subcategory = ProductSubCategorySerializer()
    design_associations = ProductDesignAssociationSerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_category', 'product_subcategory', 'description','variants','images','design_associations']
    
    
class ProductVariantGetSerializer(serializers.ModelSerializer):
    size = ProductSizeSerializer()
    product = ProductSerializer()
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'size', 'price', 'stock']