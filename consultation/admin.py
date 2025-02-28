from django.contrib import admin

# Register your models here.
from django.db import models
from django.contrib import admin

from consultation.models import ConsultationPage, ConsultationBanner

# Register the model in admin
@admin.register(ConsultationPage)
class ConsultationPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'video')




@admin.register(ConsultationBanner)
class ConsultationBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'bg_image', 'descriptions')  # Controls what columns are shown in the admin list view
    search_fields = ('title',)  # Adds a search box for the title
    list_filter = ('title',)  # Adds a filter sidebar for the title

