from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving a Message, check if it's being updated.
    If so, save the old content into MessageHistory.
    """
    if instance.id:  # existing message (not new)
        try:
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:  # content actually changed
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.sender  # tracks who edited
                )
                instance.edited = True  # mark as edited
        except Message.DoesNotExist:
            pass
