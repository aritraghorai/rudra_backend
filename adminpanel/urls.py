from django.urls import path
from adminpanel import auth_views, consultance_views, product_views, order_views

urlpatterns = [
    path('login/', auth_views.Login, name='admin_login'),
    path('logout/', auth_views.Logout, name='admin_logout'),

    # path('create/consultation-page/', consultance_views.consultation_create_or_update, name='consultation_create'),  # For create
    # path('consultation-page/<int:pk>/', consultance_views.consultation_create_or_update, name='consultation_update'),  # For update
    # path('consultation-page/list/', consultance_views.consultation_list, name='consultation_list'),  # O

    # path('consultation-banner-create/', consultance_views.consultation_banner_create_or_update, name='consultation_banner_create'),  # For create
    # path('consultation-banner/<int:pk>/', consultance_views.consultation_banner_create_or_update, name='consultation_banner_update'),  # For update
    # path('consultation-banner/list/', consultance_views.consultation_banner_list, name='consultation_banner_list'),  # O


    # path('create/who-booked-consultation/', consultance_views.who_booked_consultation_create_or_update, name='who_booked_consultation_create'),  # For create
    # path('who-booked-consultation/<int:pk>/', consultance_views.consultation_banner_create_or_update, name='who_booked_consultation_update'),  # For update
    # path('who-booked-consultation/list/', consultance_views.who_booked_consultation_list, name='who_booked_consultation_list'),  # O

    # path('consulting-expert-create/', consultance_views.consulting_expert_create_or_update, name='consulting_expert_create'),  # For create
    # path('consulting-expert/<int:pk>/', consultance_views.consulting_expert_create_or_update, name='consulting_expert_update'),  # For update
    # path('consulting-expert/list/', consultance_views.consulting_expert_list, name='consulting_expert_list'),  # O

    
    # path('consulting-plan-create/', consultance_views.consulting_plan_create_or_update, name='consulting_plan_create'),  # For create
    # path('consulting-plan/<int:pk>/', consultance_views.consulting_plan_create_or_update, name='consulting_plan_update'),  # For update
    # path('consulting-plan/list/', consultance_views.consulting_plan_list, name='consulting_plan_list'),


    path('consultations/', consultance_views.consultation_booking_list, name='consultation_booking_list'),
    
    path('toggle-status/<int:booking_id>/', consultance_views.toggle_consultation_status, name='toggle_consultation_status'),


    path('product-category-create/', product_views.product_category_create_or_update, name='product_category_create'),  # For create
    path('product-category/<int:pk>/', product_views.product_category_create_or_update, name='product_category_update'),  # For update
    path('product-category/list/', product_views.product_category_list, name='product_category_list'),
    path('product-category/delete/<int:pk>/', product_views.product_category_delete, name='product_category_delete'),


    path('faq/list/', product_views.faq_list, name='faq_list'),
    path('faq/create/', product_views.faq_create_or_update, name='faq_create'),
    path('faq/<int:pk>/', product_views.faq_create_or_update, name='faq_update'),
    path('faq/delete/<int:pk>/', product_views.faq_delete, name='faq_delete'),
    
    path('product-subcategory-create/', product_views.product_subcategory_create_or_update, name='product_subcategory_create'),  # For create
    path('product-subcategory/<int:pk>/', product_views.product_subcategory_create_or_update, name='product_subcategory_update'),  # For update
    path('product-subcategory/list/', product_views.product_subcategory_list, name='product_subcategory_list'),
    path('product-subcategory/delete/<int:pk>/', product_views.product_subcategory_delete, name='product_subcategory_delete'),

    path('product-designs-create/', product_views.product_designs_create_or_update, name='product_designs_create'),  # For create
    path('product-designs/<int:pk>/', product_views.product_designs_create_or_update, name='product_designs_update'),  # For update
    path('product-designs/list/', product_views.product_designs_list, name='product_designs_list'),
    path('product-designs/delete/<int:pk>/', product_views.product_designs_delete, name='product_designs_delete'),
    
    path('product-size-create/', product_views.product_size_create_or_update, name='product_size_create'),  # For create
    path('product-size/<int:pk>/', product_views.product_size_create_or_update, name='product_size_update'),  # For update
    path('product-size/list/', product_views.product_size_list, name='product_size_list'),
    path('product-size/delete/<int:pk>/', product_views.product_size_delete, name='product_size_delete'),
    
    path('product-create/', product_views.product_create_or_update, name='product_create'),  # For create
    path('product/<int:pk>/', product_views.product_create_or_update, name='product_update'),  # For update
    path('product/list/', product_views.product_list, name='product_list'),
    path('product/delete/<int:pk>/', product_views.product_delete, name='product_delete'),
    
    path('product/subcategories/', product_views.get_subcategories, name='get_subcategories'),
    
    path('product-image-create/', product_views.product_image_create_or_update, name='product_image_create'),  # For create
    path('product-image/<int:pk>/', product_views.product_image_create_or_update, name='product_image_update'),  # For update
    path('product-image/list/', product_views.product_image_list, name='product_image_list'),
    path('product-image/delete/<int:pk>/', product_views.product_image_delete, name='product_image_delete'),

    path('variants/list/', product_views.product_variant_list, name='product_variant_list'),
    path('variants/create/', product_views.product_variant_create_or_update, name='product_variant_create'),
    path('variants/<int:pk>/update/', product_views.product_variant_create_or_update, name='product_variant_update'),
    path('variants/<int:pk>/delete/', product_views.product_variant_delete, name='product_variant_delete'),
    
    path('orders/list/',order_views.orders_list, name='orders_list' ),

    path('orders/<int:order_id>/update-status/', order_views.update_order_status, name='update_order_status'),
]