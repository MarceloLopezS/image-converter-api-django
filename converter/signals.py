from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import ConvertedFile

@receiver(post_save, sender=ConvertedFile)
def cleanup_expired_files(sender, instance, created, **kwargs):
  expired_files = sender.objects.filter(expires_at__lt=timezone.now())

  if len(expired_files) == 0:
      return

  for file_instance in expired_files:
      if file_instance.file:
          file_instance.file.delete()
        
      file_instance.delete()