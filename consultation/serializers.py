# serializers.py
from rest_framework import serializers
from consultation.models import ConsultationBooking, ConsultationPage, ConsultationBanner, WhoBookedConsultation, ConsultingExpert, ConsultingPlan

class ConsultationPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationPage
        fields = ['title', 'image', 'video', 'descriptions', 'benefits_of_consultation', 'consult_info']

class ConsultationBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBanner
        fields = ['title', 'bg_image', 'descriptions']



class WhoBookedConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoBookedConsultation
        fields = ['title', 'icon', 'descriptions']



class ConsultingExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultingExpert
        fields = ['title', 'descriptions', 'image1', 'image2']




class ConsultingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultingPlan
        fields = ['name', 'price', 'currency']
        
        

class RudrakshaConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBooking
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']
