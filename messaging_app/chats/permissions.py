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
