from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def sent_booking_confirmation_email(customer_email, info):
    subject = 'Booking created successfully!'
    message = f'Hello! We confirm your booking for: {info}.'
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[customer_email],
        fail_silently=False,
    )
    return 'Email sent'