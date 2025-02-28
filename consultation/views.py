from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,status
from .models import ConsultationBooking, ConsultationPage, ConsultationBanner, WhoBookedConsultation, ConsultingExpert, ConsultingPlan
from .serializers import ConsultationPageSerializer, ConsultationBannerSerializer, RudrakshaConsultationSerializer, WhoBookedConsultationSerializer, ConsultingExpertSerializer, ConsultingPlanSerializer
# Create your views here.


class ConsultationPageListView(APIView):
    def get(self, request):
        consultation_pages = ConsultationPage.objects.all()
        serializer = ConsultationPageSerializer(consultation_pages, many=True)
        return Response(serializer.data)


class ConsultationBannerListView(APIView):
    def get(self, request):
        consultation_banners = ConsultationBanner.objects.all()
        serializer = ConsultationBannerSerializer(consultation_banners, many=True)
        return Response(serializer.data)



class WhoBookedConsultationListView(APIView):
    def get(self, request):
        who_booked_consultations = WhoBookedConsultation.objects.all()
        serializer = WhoBookedConsultationSerializer(who_booked_consultations, many=True)
        return Response(serializer.data)
    
class ConsultingExpertListView(APIView):
    def get(self, request):
        consulting_experts = ConsultingExpert.objects.all()
        serializer = ConsultingExpertSerializer(consulting_experts, many=True)
        return Response(serializer.data)



class ConsultingPlanListView(APIView):
    def get(self, request):
        consulting_plans = ConsultingPlan.objects.all()
        serializer = ConsultingPlanSerializer(consulting_plans, many=True)
        return Response(serializer.data)
    
class RudrakshaConsultationCreateAPIView(generics.CreateAPIView):
    queryset = ConsultationBooking.objects.all()
    serializer_class = RudrakshaConsultationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)