
from django.http import HttpResponseForbidden

class BlockSuspiciousUserAgentsMiddleware:
    """
    Middleware to block requests from suspicious user agents.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_agents = ["curl", "sqlmap", "badbot"]

    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()

        for agent in self.blocked_agents:
            if agent in user_agent:
                return HttpResponseForbidden("Forbidden: Suspicious activity detected!")

        response = self.get_response(request)
        return response
