from django.db import models
from utility.model import BaseModel
from django.contrib.auth import get_user_model
from products.models import ProductVariant, ProductDesign

User = get_user_model()

class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        db_table = 'cart'

    def get_total_amount(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    design = models.ForeignKey(ProductDesign, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_item'

    def get_total_price(self):
        base_price = self.variant.price * self.quantity
        design_price = self.design.design_price * self.quantity if self.design else 0
        return base_price + design_price

class Order(BaseModel):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    total_amount = models.PositiveIntegerField()

    class Meta:
        db_table = 'order'

class OrderItem(BaseModel):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    design = models.ForeignKey(ProductDesign, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    variant_price = models.PositiveIntegerField()  # Price at time of order
    design_price = models.PositiveIntegerField(default=0)  # Design price at time of order

    class Meta:
        db_table = 'order_item'

    def get_total_price(self):
        return (self.variant_price + self.design_price) * self.quantity
    

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100)  
    city = models.CharField(max_length=100)  
    country_code = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.address_line_1}, {self.state}"