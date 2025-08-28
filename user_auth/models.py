from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from uuid import uuid4
from user_auth.api.v1.email import send_welcome_email
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
from utils.services.otp.otp import OTPService


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError("Invalid credentials")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active',True)
    
        if not email:
            raise ValidationError("Invalid credentials")
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.EmailField(db_index=True, unique=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=250, unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=250)


    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)


    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        return super().save(*args, **kwargs)
    def set_send_otp(self):
        return OTPService.send_otp(self)

    def resend_otp(self):
        return OTPService.resend_otp(self)

    def verify_otp(self, otp):
        return OTPService.verify_otp(self, otp) and self.verified()



    def verified(self):
        """Mark user as verified and send welcome email"""
        self.is_verified = True
        self.is_active = True
        self.save(update_fields=['is_verified', 'is_active'])
        send_welcome_email(user_email=self.email, user_name=self.name)
    
    def get_email(self):
        return self.email


    def get_email(self):
        return self.email

    def delete(self):
        del self

def validate_image(image):
    max_file_size = 1 * 1024 * 1024
    if image.size > max_file_size:
        raise ValidationError("File too large! Should be under 1MB.")
    img = Image.open(image)
    if img.width > 800 or img.height > 800:
        raise ValidationError("Image dimensions should not exceed 800x800 pixels.")


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=250)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, editable=False,
                                related_name="user_profile")
    phone_number = PhoneNumberField(region="PK", unique=True, db_index=True)
    profile_pic = models.ImageField(validators=[validate_image])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = False


class Address(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=False, related_name="user_address")
    country = models.CharField(max_length=250, db_index=True,default="Pakistan")
    state = models.CharField(max_length=250, db_index=True)
    city = models.CharField(max_length=250, db_index=True)
    street = models.CharField(max_length=250, db_index=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = False

    def __str__(self):
        return f" Country: {self.country} State: {self.state} City: {self.city} Street:{self.street} "

