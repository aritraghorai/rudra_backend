from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User
from orders.models import Cart

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    print('cart initialized')
    if created:
        Cart.objects.create(user=instance)
