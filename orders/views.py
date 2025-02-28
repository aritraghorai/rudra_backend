import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CartItem, Cart, Order, OrderItem,ShippingAddress
from products.models import ProductVariant
from .serializers import CartItemSerializer, CartSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db import transaction

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related(
        "items__variant__product"
    )
        
    @action(detail=False, methods=['post'])
    def manage_item(self, request):
        cart = request.user.cart
        variant_id = request.data.get('variant')
        design_id = request.data.get('design') or None
        quantity = int(request.data.get('quantity', 0))
        
        
        try:
            variant = ProductVariant.objects.get(id=variant_id)
            
            cart_item = CartItem.objects.filter(
                cart=cart,
                variant_id=variant_id,
                design_id=design_id
            ).first()
            
            if cart_item:
                new_quantity = cart_item.quantity + quantity
                if new_quantity <= 0:
                    cart_item.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                    
                if variant.stock < new_quantity:
                    return Response(
                        {"error": "Not enough stock"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                if quantity <= 0:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                    
                if variant.stock < quantity:
                    return Response(
                        {"error": "Not enough stock"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                cart_item = CartItem.objects.create(
                    cart=cart,
                    variant_id=variant_id,
                    design_id=design_id,
                    quantity=quantity
                )
            
            return Response(CartItemSerializer(cart_item).data)

        except ProductVariant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            user=request.user,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            total_amount=cart.get_total_amount(),
            shipping_address=request.data.get('shipping_address'),
            contact_number=request.data.get('contact_number')
        )
        
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                variant=cart_item.variant,
                design=cart_item.design,
                quantity=cart_item.quantity,
                variant_price=cart_item.variant.price,
                design_price=cart_item.design.design_price if cart_item.design else 0
            )
            
            cart_item.variant.stock -= cart_item.quantity
            cart_item.variant.save()
        
        cart.items.all().delete()
        cart.save()
        
        return Response(OrderSerializer(order).data)



from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, Order, OrderItem, ShippingAddress, ProductVariant

class PaymentSuccessView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        order_id = data.get('orderId')
        shipping_address = data.get('address')
        cart_id = data.get('cartId')
        
        cart = get_object_or_404(Cart, id=cart_id)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"detail": "Cart is empty or invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            
            total_amount = sum(item.get_total_price() for item in cart_items)
    
            order = Order.objects.create(
                user=cart.user,
                order_number=str(order_id),  
                status='CONFIRMED',
                total_amount=total_amount
            )

            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    design=item.design,
                    quantity=item.quantity,
                    variant_price=item.variant.price,
                    design_price=item.design.design_price if item.design else 0
                )

                
                variant = item.variant
                variant.stock -= item.quantity
                variant.save()

            
            ShippingAddress.objects.create(
                order=order,
                address_line_1=shipping_address.get('address_line_1'),
                address_line_2=shipping_address.get('address_line_2', ''),
                state=shipping_address.get('admin_area_1'),
                city=shipping_address.get('admin_area_2'),
                country_code=shipping_address.get('country_code'),
                postal_code=shipping_address.get('postal_code'),
            )

            
            cart.items.all().delete()

        
        return Response({
            "message": "Order successfully created and stock updated.",
            "order_id": order.id,
            "order_number": order.order_number
        }, status=status.HTTP_201_CREATED)
        
        
class MyOrdersView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)\
            .select_related('user')\
            .prefetch_related(
                'items__variant__product__images',
                'items__variant__size',
                'items__design'
            )\
            .order_by('-created_at')
        
        response_data = [{
            'id': order.id,
            'order_number': order.order_number,
            'status': order.status,
            'total_amount': order.total_amount,
            'created_at': order.created_at,
            'items': [{
                'id': item.id,
                'quantity': item.quantity,
                'variant': {
                    'product': {
                        'product_name': item.variant.product.product_name,
                        'images': [{
                            'image': image.image.url
                        } for image in item.variant.product.images.all()]
                    },
                    'size': {
                        'size_name': item.variant.size.size_name
                    }
                },
                'design': {
                    'design_name': item.design.design_name
                } if item.design else None
            } for item in order.items.all()]
        } for order in orders]

        return Response(response_data)
