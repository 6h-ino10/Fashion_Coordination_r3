from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from users.models import UserProfile
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

#@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f'UserProfile created for user:{instance.username}')

#@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.userprofile.save()
    logger.info(f'UserProfile saved for user:{instance.username}')