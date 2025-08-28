
import time
import logging

logger = logging.getLogger(__name__)

class RequestTimerMiddleware:
    """
    Middleware to measure how long each request takes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        logger.info(f"{request.path} took {duration:.2f} seconds.")

        return response
