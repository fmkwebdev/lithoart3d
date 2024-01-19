import uuid

class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.nonce = str(uuid.uuid4())
        response = self.get_response(request)
        return response