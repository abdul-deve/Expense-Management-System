from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
import pyotp
from django.utils import timezone
from django.conf import settings


class EmailOTPDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp_device")
    secret_key = models.CharField(max_length=16, default=pyotp.random_base32, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_attempt = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(default=0, validators=[MaxValueValidator(3)])
    cooldown_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"EmailOTPDevice for {self.user.email}"

    def is_in_cooldown(self):
        if self.cooldown_until:
            return timezone.now() < self.cooldown_until
        return False

    def set_cooldown(self, seconds=None):
        if seconds is None:
            seconds = getattr(settings, "OTP_COOLDOWN_SECONDS", 0)
        self.cooldown_until = timezone.now() + timezone.timedelta(seconds=seconds)
        self.save(update_fields=["cooldown_until"])
