from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own conversations/messages.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming your Message model has a `sender` field
        # and Conversation model has a `participants` relation
        if hasattr(obj, 'sender'):  
            return obj.sender == request.user
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users
    - Only participants in a conversation can send/view/update/delete messages
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be either a Conversation or a Message.
        - If it's a Conversation: check if user is in participants
        - If it's a Message: check if user is in participants of the related conversation
        """
        if hasattr(obj, "participants"):  # Conversation model
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):  # Message model
            return request.user in obj.conversation.participants.all()

        return False