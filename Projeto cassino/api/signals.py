from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import BetAccount

User = get_user_model()

@receiver(post_save, sender=User)
def create_bet_account(sender, instance, created, **kwargs):
    if created:
        BetAccount.objects.create(user=instance)
