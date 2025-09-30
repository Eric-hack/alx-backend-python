from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # 🔑 New field for threaded replies
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"

    # Recursive function to fetch threaded replies
    def get_thread(self):
        """Recursively fetch this message and all replies in threaded format"""
        thread = {
            "id": self.id,
            "sender": self.sender.username,
            "receiver": self.receiver.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "replies": [reply.get_thread() for reply in self.replies.all()],
        }
        return thread


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name="history", on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"
