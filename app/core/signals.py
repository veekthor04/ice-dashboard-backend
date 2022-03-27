from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Payment


@receiver(post_save, sender=Payment)
def post_save_transfer_created_receiver(
    sender, instance: Payment, created, **kwargs
) -> None:
    """
    Update Related Customer's Balance
    """
    if created:
        instance.update_customer_balance()
