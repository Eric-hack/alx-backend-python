#!/usr/bin/env python3
"""ViewSets for conversations and messages in chats app."""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating conversations."""

    queryset = Conversation.objects.all().prefetch_related("participants", "message_set")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants."""
        participants_ids = request.data.get("participants", [])
        participants = User.objects.filter(user_id__in=participants_ids)

        if not participants.exists():
            return Response(
                {"error": "At least one valid participant is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """Get all messages in a conversation."""
        conversation = self.get_object()
        messages = conversation.message_set.all().order_by("sent_at")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating messages."""

    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """Send a message to an existing conversation."""
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body")

        if not all([conversation_id, sender_id, message_body]):
            return Response(
                {"error": "conversation, sender, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        sender = get_object_or_404(User, user_id=sender_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body,
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
