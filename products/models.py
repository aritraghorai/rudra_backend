from django.db import models
from utility.model import BaseModel


class ProductCategory(BaseModel):
    category_name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='product/images/', null=True, blank=True)
    descriptions = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'product_category'
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.category_name


class ProductSubCategory(BaseModel):
    category = models.ForeignKey(
        'ProductCategory', 
        on_delete=models.CASCADE, 
        related_name='subcategories'
    )
    subcategory_name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='product/images/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'product_subcategory'
        verbose_name = "Product Subcategory"
        verbose_name_plural = "Product Subcategories"

    def __str__(self):
        return self.subcategory_name


class ProductDesign(BaseModel):
    design_name = models.CharField(max_length=500)
    design_image = models.ImageField(upload_to='product/images/', null=True, blank=True)
    design_icon = models.ImageField(upload_to='product/images/', null=True, blank=True)
    design_description = models.TextField(blank=True, null=True)
    design_price = models.PositiveIntegerField(default=0)  

    class Meta:
        db_table = 'product_design'
        verbose_name = "Product Design"
        verbose_name_plural = "Product Designs"

    def __str__(self):
        return self.design_name


class ProductSize(BaseModel):
    size_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'product_size'
        verbose_name = "Product Size"
        verbose_name_plural = "Product Sizes"

    def __str__(self):
        return self.size_name


class Product(BaseModel):
    product_name = models.CharField(max_length=500)
    product_category = models.ForeignKey(
        'ProductCategory', 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    product_subcategory = models.ForeignKey(
        'ProductSubCategory', 
        on_delete=models.CASCADE, 
        related_name='products', null=True, blank=True
    )
    
    beej_mantra=models.TextField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'product'
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name


class ProductVariant(BaseModel):
    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='variants'
    )
    size = models.ForeignKey(
        'ProductSize', 
        on_delete=models.SET_NULL, 
        related_name='variants', 
        null=True, blank=True
    )
    price = models.PositiveIntegerField(default=0)  
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'product_variant'
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        return f"{self.product.product_name} - {self.size.size_name if self.size else 'Default'}"


class ProductDesignAssociation(BaseModel):
    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='design_associations'
    )
    design = models.ForeignKey(
        'ProductDesign', 
        on_delete=models.CASCADE, 
        related_name='design_associations'
    )

    class Meta:
        db_table = 'product_design_association'
        verbose_name = "Product Design Association"
        verbose_name_plural = "Product Design Associations"

    def __str__(self):
        return f"{self.product.product_name} - {self.design.design_name}"


class ProductImage(BaseModel):
    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='product/images/', null=True, blank=True)

    class Meta:
        db_table = 'product_image'
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return self.product.product_name


class FAQ(BaseModel):
    image = models.ImageField(upload_to='faq/images/', null=True, blank=True)
    question = models.CharField(max_length=255)  
    answer = models.TextField()  
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='faq_items')  



    def __str__(self):
        return self.question