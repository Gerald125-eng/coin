from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile,Deposit,Withdrawal
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



@receiver(post_save, sender=Deposit)
def send_approval_email(sender, instance, created, **kwargs):
    if not created:
        # Check if status changed to approved
        if instance.status == "approved":
            send_mail(
                "Deposit Approved",
                f"Dear {instance.user.username}, your deposit of ${instance.amount} into {instance.plan.name} has been approved!",
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
                fail_silently=False,
            )


@receiver(post_save, sender=Withdrawal)
def send_withdrawal_approval_email(sender, instance, created, **kwargs):
    if not created:
        if instance.status == "approved":
            send_mail(
                "Withdrawal Approved",
                f"Dear {instance.user.username}, your withdrawal of ${instance.amount} has been approved and processed.",
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
                fail_silently=False,
            )