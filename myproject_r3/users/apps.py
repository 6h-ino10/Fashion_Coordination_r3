from django.apps import AppConfig
from django.db.models.signals import post_save
#from django.contrib.auth.models import User
#from django.dispatch import receiver
#from .models import UserProfile


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth import get_user_model
        from users.models import UserProfile
        from users.signals import create_user_profile, save_user_profile
        #import users.signals

        User = get_user_model()
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)
