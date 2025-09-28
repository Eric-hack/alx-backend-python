# chats/middleware.py
import os
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Path to parent directory of this file
        self.log_file_path = os.path.join(settings.BASE_DIR, 'requests.log')

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open(self.log_file_path, "a") as log_file:
            log_file.write(log_entry)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict access to chat app endpoints
        if request.path.startswith('/api/'):  
            current_hour = datetime.now().hour
            if current_hour < 6 or current_hour >= 21:  
                return HttpResponseForbidden("Chat access is restricted between 9 PM and 6 AM.")

        response = self.get_response(request)
        return response