from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from consultation.models import ConsultationBooking, ConsultationPage, ConsultationBanner, WhoBookedConsultation, ConsultingExpert, ConsultingPlan
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  

def consultation_create_or_update(request, pk=None):
    consultation_page = None
    if pk:
        consultation_page = get_object_or_404(ConsultationPage, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', consultation_page.title if consultation_page else '')
        descriptions = request.POST.get('descriptions', consultation_page.descriptions if consultation_page else '')
        benefits_of_consultation = request.POST.get('benefits_of_consultation', consultation_page.benefits_of_consultation if consultation_page else '')
        consult_info = request.POST.get('consult_info', consultation_page.consult_info if consultation_page else '')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        
        if not title:
            messages.error(request, 'Title is required.')
        else:
            if consultation_page:
                
                consultation_page.title = title
                consultation_page.descriptions = descriptions
                consultation_page.benefits_of_consultation = benefits_of_consultation
                consultation_page.consult_info = consult_info
                if image:
                    consultation_page.image = image
                if video:
                    consultation_page.video = video
                consultation_page.save()
                messages.success(request, 'Consultation Page updated successfully!')
                return redirect('consultation_list') 
            elif ConsultationPage.objects.all().exists():
                consultation_page=ConsultationPage.objects.first()
                
                consultation_page.title = title
                consultation_page.descriptions = descriptions
                consultation_page.benefits_of_consultation = benefits_of_consultation
                consultation_page.consult_info = consult_info
                if image:
                    consultation_page.image = image
                if video:
                    consultation_page.video = video
                consultation_page.save()
                messages.success(request, 'Consultation Page updated successfully!')
                return redirect('consultation_list') 

            else:
                
                ConsultationPage.objects.create(
                    title=title,
                    image=image,
                    video=video,
                    descriptions=descriptions,
                    benefits_of_consultation=benefits_of_consultation,
                    consult_info=consult_info
                )
                messages.success(request, 'Consultation Page created successfully!')
            return redirect('consultation_list')  

    return render(request, 'consultation/consultation_page_form.html', {'consultation_page': consultation_page})


def consultation_list(request):
    consultations = ConsultationPage.objects.all()
    return render(request, 'consultation/consultation_page_list.html', {'consultations': consultations})



def consultation_banner_create_or_update(request, pk=None):
    
    consultation_banner= None
    if pk:
        consultation_banner = get_object_or_404(ConsultationBanner, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', consultation_banner.title if consultation_banner else '')
        descriptions = request.POST.get('descriptions', consultation_banner.descriptions if consultation_banner else '')
        bg_image = request.FILES.get('bg_image')
        

        
        if not title:
            messages.error(request, 'Title is required.')
        else:
            if consultation_banner:
                
                consultation_banner.title = title
                consultation_banner.descriptions = descriptions
               
                if bg_image:
                    consultation_banner.bg_image = bg_image
               
                consultation_banner.save()
                messages.success(request, 'Consultation banner updated successfully!')
                return redirect('consultation_banner_list') 
            else:
                
                ConsultationBanner.objects.create(
                    title=title,
                    bg_image=bg_image,
                    descriptions=descriptions,
                )
                messages.success(request, 'Consultation Page created successfully!')
            return redirect('consultation_banner_list')  

    return render(request, 'consultation/consultation_banner_form.html', {'consultation_banner': consultation_banner})



def consultation_banner_list(request):
    consultations_banner = ConsultationBanner.objects.all()
    return render(request, 'consultation/consultation_banner_list.html', {'consultations_banner': consultations_banner})




def who_booked_consultation_create_or_update(request, pk=None):
    
    who_booked_consultation= None
    if pk:
        who_booked_consultation = get_object_or_404(WhoBookedConsultation, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', who_booked_consultation.title if who_booked_consultation else '')
        descriptions = request.POST.get('descriptions', who_booked_consultation.descriptions if who_booked_consultation else '')
        icon = request.FILES.get('icon')
        

        
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('who_booked_consultation_create')
        else:
            if who_booked_consultation:
                
                who_booked_consultation.title = title
                who_booked_consultation.descriptions = descriptions
               
                if icon:
                    who_booked_consultation.icon = icon
               
                who_booked_consultation.save()
                messages.success(request, 'Who booked Consultation data updated successfully!')
                return redirect('who_booked_consultation_list') 
            else:
                
                WhoBookedConsultation.objects.create(
                    title=title,
                    icon=icon,
                    descriptions=descriptions,
                )
                messages.success(request, 'Who booked Consultation data created successfully!')
            return redirect('who_booked_consultation_list')  

    return render(request, 'consultation/who_booked_consultation_form.html', {'who_booked_consultation': who_booked_consultation})



def who_booked_consultation_list(request):
    who_booked_consultation = WhoBookedConsultation.objects.all()
    return render(request, 'consultation/who_booked_consultation_list.html', {'who_booked_consultation': who_booked_consultation})





def consulting_expert_create_or_update(request, pk=None):
    
    consulting_expert= None
    if pk:
        consulting_expert= get_object_or_404(ConsultingExpert, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', consulting_expert.title if consulting_expert else '')
        descriptions = request.POST.get('descriptions', consulting_expert.descriptions if consulting_expert else '')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        

        
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('consulting_expert_create')
        else:
            if consulting_expert:
                
                consulting_expert.title = title
                consulting_expert.descriptions = descriptions
               
                if image1:
                    consulting_expert.image1 = image1
                if image2:
                    consulting_expert.image2 = image2
                consulting_expert.save()
                messages.success(request, 'consulting expert data updated successfully!')
                return redirect('consulting_expert_list') 
            else:
                
                ConsultingExpert.objects.create(
                    title=title,
                    image1=image1,
                    image2=image2,
                    descriptions=descriptions,
                )
                messages.success(request, 'consulting expert data created successfully!')
            return redirect('consulting_expert_list')  

    return render(request, 'consultation/consulting_expert_form.html', {'consulting_expert': consulting_expert})



def consulting_expert_list(request):
    consulting_expert= ConsultingExpert.objects.all()
    return render(request, 'consultation/consulting_expert_list.html', {'consulting_expert': consulting_expert})


def consulting_plan_create_or_update(request, pk=None):
    
    consulting_plan= None
    if pk:
        consulting_plan= get_object_or_404(ConsultingPlan, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', consulting_plan.name if consulting_plan else '')
        price = request.POST.get('price', consulting_plan.price if consulting_plan else 0)
        currency = request.POST.get('currency', consulting_plan.currency if consulting_plan else "USD")
        

        
        if not name:
            messages.error(request, 'name is required.')
            return redirect('consulting_plan_create')
        else:
            if consulting_plan:
                
                consulting_plan.name = name
                consulting_plan.price = price
                consulting_plan.currency=currency
                consulting_plan.save()
                messages.success(request, 'consulting plan data updated successfully!')
                return redirect('consulting_plan_list') 
            else:
                
                ConsultingPlan.objects.create(
                    name=name,
                    price=price,
                    currency=currency
                )
                messages.success(request, 'consulting expert data created successfully!')
            return redirect('consulting_plan_list')  

    return render(request, 'consultation/consulting_plan_form.html', {'consulting_plan': consulting_plan})



def consulting_plan_list(request):
    consulting_plan= ConsultingPlan.objects.all()
    return render(request, 'consultation/consulting_plan_list.html', {'consulting_plan': consulting_plan})


def consultation_booking_list(request):
    consultation_booking = ConsultationBooking.objects.all()
    return render(request, 'consultation/booking/consultation_booking_list.html', {'booking_list': consultation_booking})
    

@require_POST
@csrf_exempt  
def toggle_consultation_status(request, booking_id):
    print(f"Received request for booking_id: {booking_id}")  
    try:
        booking = ConsultationBooking.objects.get(id=booking_id)
        booking.completed = not booking.completed
        booking.save()
        return JsonResponse({
            'success': True,
            'completed': booking.completed
        })
    except ConsultationBooking.DoesNotExist:
        print(f"Booking {booking_id} not found")  
        return JsonResponse({
            'success': False,
            'error': 'Booking not found'
        }, status=404)