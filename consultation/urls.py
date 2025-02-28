# urls.py
from django.urls import path
from consultation import views

urlpatterns = [
    path('consultations-page/', views.ConsultationPageListView.as_view(), name='consultation-list'),
    path('consultation-banners/', views.ConsultationBannerListView.as_view(), name='consultation-banner-list'),
    path('who-booked-consultations/', views.WhoBookedConsultationListView.as_view(), name='who-booked-consultation-list'),
    path('consulting-experts/', views.ConsultingExpertListView.as_view(), name='consulting-expert-list'),
    path('consulting-plans/', views.ConsultingPlanListView.as_view(), name='consulting-plan-list'),
    path('booking/create/', views.RudrakshaConsultationCreateAPIView.as_view(), name='consultation-create'),

]
