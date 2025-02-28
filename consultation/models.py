from django.db import models
from utility.model import BaseModel


class ConsultationPage(BaseModel):
    title = models.CharField(max_length=1000, blank=True)
    image = models.FileField(upload_to='consultation/images/', null=True, blank=True)  
    video = models.FileField(upload_to='consultation/videos/', null=True, blank=True)  
    descriptions = models.TextField(blank=True, null=True)
    benefits_of_consultation=models.TextField(blank=True, null=True)
    consult_info=models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title if self.title else "Untitled Banner"
    class Meta:
        db_table = 'consultation_page'
        verbose_name = "Consultation Page"
        verbose_name_plural = "Consultation Page"



class ConsultationBanner(BaseModel):
    title = models.CharField(max_length=1000, blank=True)
    bg_image = models.FileField(upload_to='consultation/images/', null=True, blank=True)  
    descriptions = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title if self.title else "Untitled Banner"
    class Meta:
        db_table = 'consultation_banner'
        verbose_name = "Consultation Banner"
        verbose_name_plural = "Consultation Banner"



class WhoBookedConsultation(BaseModel):
    title = models.CharField(max_length=1000, blank=True)
    icon= models.FileField(upload_to='consultation/images/', null=True, blank=True)  
    descriptions = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title if self.title else "Untitled Banner"
    class Meta:
        db_table = 'who_booked_consultation'
        verbose_name = "Who Booked Consultation"
        verbose_name_plural = "Who Booked Consultation"


class ConsultingExpert(BaseModel):
    title = models.CharField(max_length=1000, blank=True)
    descriptions = models.TextField(blank=True, null=True)
    image1 = models.FileField(upload_to='consultation/images/', null=True, blank=True)  
    image2 = models.FileField(upload_to='consultation/images/', null=True, blank=True)
    def __str__(self):
        return self.title if self.title else "Untitled Banner"
    class Meta:
        db_table = 'consulting_expert'
        verbose_name = "ConsultingExpert"
        verbose_name_plural = "ConsultingExpert"

class ConsultingPlan(BaseModel):
    name = models.CharField(max_length=500, blank=True)
    price=models.PositiveBigIntegerField(default=0)
    currency=models.CharField(max_length=100)
    class Meta:
        db_table = 'consulting_plan'
        verbose_name = "ConsultingPlan"
        verbose_name_plural = "ConsultingPlans"

class ConsultationBooking(BaseModel):
    first_name=models.CharField(max_length=500)
    last_name=models.CharField(max_length=200)
    email=models.EmailField()
    phone_number = models.CharField(max_length=15)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'rudraksha_consultation_with_rudraksha_expert_book'
        verbose_name = "Rudraksha_Consultation_with_Rudraksha_Expert_Book"
        verbose_name_plural = "Rudraksha_Consultation_with_Rudraksha_Expert_Book"


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
