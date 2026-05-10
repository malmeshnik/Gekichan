from django.utils import timezone
from .models import User

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # We use update() to avoid triggering signals or full model save
            User.objects.filter(pk=request.user.pk).update(last_activity_at=timezone.now())

        response = self.get_response(request)
        return response
