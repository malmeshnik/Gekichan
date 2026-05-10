from django.utils import timezone
from apps.users.models import User

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # We use update() to avoid triggering signals or auto_now fields if not desired
            # But since it's just one field, it's fine.
            User.objects.filter(id=request.user.id).update(last_activity_at=timezone.now())

        response = self.get_response(request)
        return response
