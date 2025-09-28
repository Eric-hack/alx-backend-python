import logging
import os
from datetime import datetime
from django.conf import settings

# Path for the log file inside the chats app
LOG_FILE_PATH = os.path.join(settings.BASE_DIR, 'chats', 'requests.log')

# Ensure the directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Configure the logger
logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers if middleware reloads
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """Middleware to log each user's request with timestamp, user, and path."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        path = request.path
        timestamp = datetime.now()

        # Log the request to chats/requests.log
        logger.info(f"{timestamp} - User: {user} - Path: {path}")

        # Continue processing the request
        response = self.get_response(request)
        return response
