# chats/middleware.py
import os
from datetime import datetime
from django.conf import settings

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
