from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings
from utils.models import EmailOTPDevice
import pyotp

OTPServiceError = type("OTPServiceError", (Exception,), {})
UserAlreadyVerified = type("UserAlreadyVerified", (OTPServiceError,), {})
OTPDeviceNotFound = type("OTPDeviceNotFound", (OTPServiceError,), {})
InvalidOTP = type("InvalidOTP", (OTPServiceError,), {})
CooldownError = type("CooldownError", (OTPServiceError,), {})
MaxAttemptsError = type("MaxAttemptsError", (OTPServiceError,), {})


class OTPService:
    @staticmethod
    def _get_or_create_device(user):
        device = EmailOTPDevice.objects.filter(user=user).first()
        if device:
            EmailOTPDevice.objects.filter(user=user).exclude(pk=device.pk).delete()
        else:
            device = EmailOTPDevice.objects.create(user=user)

        if device.attempts is None:
            device.attempts = 0
        if device.last_attempt is None:
            device.last_attempt = None
        if device.cooldown_until is None:
            device.cooldown_until = timezone.now()

        device.save(update_fields=["attempts", "last_attempt", "cooldown_until"])
        return device

    @staticmethod
    def send_otp(user, extra_context=None):
        device = OTPService._get_or_create_device(user)
        if device.attempts >= 3:
            raise MaxAttemptsError("Maximum OTP attempts reached")

        if device.is_in_cooldown():
            remaining = int((device.cooldown_until - timezone.now()).total_seconds())
            raise CooldownError(f"Wait {remaining} seconds before retrying")

        return OTPService._deliver_otp(device, extra_context)

    @staticmethod
    def resend_otp(user, extra_context=None):
        device = OTPService._get_or_create_device(user)

        if device.is_in_cooldown():
            remaining = int((device.cooldown_until - timezone.now()).total_seconds())
            return {"resent": False, "message": f"Please wait {remaining} seconds before requesting OTP again"}

        device.attempts = 0
        device.last_attempt = None
        device.save(update_fields=["attempts", "last_attempt"])

        return OTPService._deliver_otp(device, extra_context, resend=True)

    @staticmethod
    def _deliver_otp(device, extra_context=None, resend=False):
        totp = pyotp.TOTP(device.secret_key, digits=6, interval=300)
        token = totp.now()

        context = {"otp": token, "user": device.user}
        if extra_context:
            context.update(extra_context)

        template_path = getattr(settings, "OTP_EMAIL_TEMPLATE", "email_templates/otp_email.html")
        body_html = get_template(template_path).render(context)

        subject = getattr(settings, "OTP_EMAIL_SUBJECT", "Your OTP Code")
        from_email = getattr(settings, "OTP_EMAIL_SENDER", settings.DEFAULT_FROM_EMAIL)

        email = EmailMessage(subject, body_html, from_email, [device.user.email])
        email.content_subtype = "html"
        email.send(fail_silently=False)

        device.last_attempt = timezone.now()
        device.set_cooldown()
        device.save(update_fields=["last_attempt", "cooldown_until"])

        return {"sent": True, "resend": resend, "message": "OTP sent successfully"}

    @staticmethod
    def verify_otp(user, token):
        try:
            device = EmailOTPDevice.objects.get(user=user)
        except EmailOTPDevice.DoesNotExist:
            raise OTPDeviceNotFound("OTP device not found")

        totp = pyotp.TOTP(device.secret_key, digits=6, interval=300)
        if totp.verify(token):
            device.secret_key = pyotp.random_base32()
            device.attempts = 0
            device.last_attempt = None
            device.cooldown_until = None
            device.save(update_fields=["secret_key", "attempts", "last_attempt", "cooldown_until"])
            return {"verified": True, "message": "OTP verified successfully"}
        else:
            device.attempts += 1
            device.last_attempt = timezone.now()
            device.set_cooldown()
            device.save(update_fields=["attempts", "last_attempt", "cooldown_until"])
            if device.attempts > 3:
                raise MaxAttemptsError("Maximum OTP attempts reached")
            raise InvalidOTP("Invalid OTP code")

    @staticmethod
    def can_attempt(user):
        try:
            device = EmailOTPDevice.objects.get(user=user)
        except EmailOTPDevice.DoesNotExist:
            return True
        return device.attempts > 3 and not device.is_in_cooldown()
