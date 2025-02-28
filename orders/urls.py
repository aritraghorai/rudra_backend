from .views import CartViewSet, OrderViewSet,PaymentSuccessView,MyOrdersView
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = router.urls + [
        path('payment/', PaymentSuccessView.as_view(), name='payment-success'),
        path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
]


