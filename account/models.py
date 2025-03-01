from django.db import models

# Create your models here.
from django.db import models

from base64 import b32encode
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager

from django.template.defaultfilters import slugify
from base64 import b32encode
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from utility.model import BaseModel


# Create your models here.
class CustomUserManager(UserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Phone must be set"))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given phone and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


def media_directory_path(instance, filename):
    return "rudrakha/user".format(filename)


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=21, null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True)
    gender = models.CharField(
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
        max_length=74,
        null=True,
        blank=True,
    )
    accepts_marketing = models.CharField(
        choices=(("Yes", "Yes"), ("No", "No")), max_length=74, default="Yes"
    )
    profile_pic = models.FileField(
        upload_to=media_directory_path, max_length=1000, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def hash(self):
        return b32encode(("74-%s-base32secret" % self.email).encode("utf-8"))


class OTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp")
    otp = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.otp

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
