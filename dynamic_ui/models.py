from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.db.models import JSONField


class Profile(models.Model):
    page_name = models.CharField(max_length=200, unique=True)
    data = JSONField()

    def __str__(self):
        return self.name


class PageImage(models.Model):
    page = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="page_images/")

    def __str__(self):
        return self.page

    class Meta:
        verbose_name = "Page Image"
        verbose_name_plural = "Page Images"
        ordering = ["page"]


class PageVideo(models.Model):
    page = models.ForeignKey(Profile, on_delete=models.CASCADE)
    video = models.FileField(upload_to="page_videos/")

    def __str__(self):
        return self.page

    class Meta:
        verbose_name = "Page Video"
        verbose_name_plural = "Page Videos"
        ordering = ["page"]
