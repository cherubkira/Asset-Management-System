from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Asset, AssignmentHistory

@receiver(post_save, sender=Asset)
def auto_record_assignment(sender, instance, created, **kwargs):
    if created:
        
        if instance.assigned_to:
            AssignmentHistory.objects.create(
                asset=instance,
                assigned_from=None,
                assigned_to=instance.assigned_to,
                note="Initial assignment on asset creation"
            )
    else:
       
        old = sender.objects.get(pk=instance.pk)
        if old.assigned_to != instance.assigned_to:
            AssignmentHistory.objects.create(
                asset=instance,
                assigned_from=old.assigned_to,
                assigned_to=instance.assigned_to,
                note="Re-assigned automatically by signal"
            )
