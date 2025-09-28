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

class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of messages a user can send per minute based on IP.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Store message timestamps for each IP
        self.message_log = {}

    def __call__(self, request):
        # Only track POST requests to the chat endpoint
        if request.method == 'POST' and request.path.startswith('/api/'):  # adjust path if needed
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 1 minute time window
            limit = 5  # max 5 messages per minute

            # Initialize list if IP not in log
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Remove timestamps outside the window
            self.message_log[ip] = [t for t in self.message_log[ip] if now - t < window]

            # Check if limit exceeded
            if len(self.message_log[ip]) >= limit:
                return HttpResponseForbidden("You have exceeded the message limit. Please wait before sending more messages.")

            # Record the new message timestamp
            self.message_log[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Get client IP address from request headers.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip