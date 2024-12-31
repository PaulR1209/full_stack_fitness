from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Order


@receiver(post_save, sender=Order)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Fullstack Fitness!"

        start_date = instance.created_at.strftime("%B %d, %Y")
        renewal_date = instance.next_renewal.strftime("%B %d, %Y")

        body = f"""
            <h1>Welcome, {instance.user}!</h1>
            <p>Thank you for signing up for Fullstack Fitness! Your membership is now active.</p>
            <p><strong>Membership Type:</strong> {instance.membership}</p>
            <p><strong>Start Date:</strong> {start_date}</p>
            <p><strong>Renewal Date:</strong> {renewal_date}</p>
            <p><strong>Price:</strong> {instance.total_next_payment}</p>
        """
    else:
        subject = "Your Membership Details Have Been Updated"

        start_date = instance.created_at.strftime("%B %d, %Y")
        renewal_date = instance.next_renewal.strftime("%B %d, %Y")

        body = f"""
            <h1>Hi {instance.user},</h1>
            <p>Your membership details have been updated. Here are your new details:</p>
            <p><strong>Membership Type:</strong> {instance.membership}</p>
            <p><strong>Start Date:</strong> {instance.created_at}</p>
            <p><strong>Renewal Date:</strong> {instance.next_renewal}</p>
            <p><strong>Price:</strong> {instance.total_next_payment}</p>
        """

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[instance.user.email],
    )
    email.content_subtype = "html"
    email.send()
