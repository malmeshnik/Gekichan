from django.utils import timezone
from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from .models import FocusSession
from .serializers import FocusSessionSerializer

class FocusSessionViewSet(viewsets.ModelViewSet):
    serializer_class = FocusSessionSerializer

    def get_queryset(self):
        return FocusSession.objects.filter(user=self.request.user)

    @decorators.action(detail=False, methods=['post'])
    def start(self, request):
        user = request.user
        # Check for active session
        if FocusSession.objects.filter(user=user, end_time__isnull=True).exists():
            return Response(
                {"error": "You already have an active session."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, start_time=timezone.now())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=['patch'])
    def stop(self, request, pk=None):
        session = self.get_object()
        if session.end_time:
            return Response(
                {"error": "Session already stopped."},
                status=status.HTTP_400_BAD_REQUEST
            )

        session.end_time = timezone.now()
        duration_delta = session.end_time - session.start_time
        session.duration = int(duration_delta.total_seconds())
        session.save()

        serializer = self.get_serializer(session)
        return Response(serializer.data)
