import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import EmployeeProfile

@receiver(post_delete, sender=EmployeeProfile)
def delete_profile_picture_on_delete(sender, instance, **kwargs):
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)

@receiver(pre_save, sender=EmployeeProfile)
def delete_old_profile_picture_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New instance, nothing to do

    try:
        old_file = EmployeeProfile.objects.get(pk=instance.pk).profile_picture
    except EmployeeProfile.DoesNotExist:
        return

    new_file = instance.profile_picture
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)