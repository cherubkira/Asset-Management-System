# assets/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Asset, AssignmentHistory

@receiver(pre_save, sender=Asset)
def auto_record_assignment(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = sender.objects.filter(pk=instance.pk).first()
    if old and old.assigned_to != instance.assigned_to:
        AssignmentHistory.objects.create(asset=instance, assigned_from=old.assigned_to, assigned_to=instance.assigned_to, note="Recorded by signal")
