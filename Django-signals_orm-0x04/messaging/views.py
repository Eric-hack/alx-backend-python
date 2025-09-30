from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Message

@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their account.
    """
    user = request.user
    user.delete()
    return redirect("/")  # redirect to homepage or login page after deletion

@login_required
def conversation_list(request):
    """
    Retrieve all top-level messages and their threaded replies.
    Optimized with select_related and prefetch_related.
    """
    messages = (
        Message.objects.filter(receiver=request.user) 
        .select_related("sender", "receiver")         
        .prefetch_related("replies__sender", "replies__receiver") 
    )

    data = [message.get_thread() for message in messages]
    return JsonResponse(data, safe=False)


@login_required
def send_message(request, receiver_id):
    """
    Example view for sending a new message (to show sender=request.user).
    """
    from django.contrib.auth.models import User
    import json

    if request.method == "POST":
        body = json.loads(request.body)
        receiver = get_object_or_404(User, id=receiver_id)
        parent_message_id = body.get("parent_message")

        parent_message = None
        if parent_message_id:
            parent_message = get_object_or_404(Message, id=parent_message_id)

        message = Message.objects.create(
            sender=request.user,               
            receiver=receiver,                  
            content=body["content"],
            parent_message=parent_message,
        )

        return JsonResponse({"id": message.id, "content": message.content})

    return JsonResponse({"error": "Invalid request"}, status=400)
