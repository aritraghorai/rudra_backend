from django.urls import path
from . import views


urlpatterns = [
    path('variants/',views.ProductsListView.as_view()),
    path('category/',views.CategoryListView.as_view()),
    path('faq/<int:pk>/',views.FAQListView.as_view()),
]
