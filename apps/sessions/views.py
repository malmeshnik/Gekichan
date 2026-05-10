from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from .models import FocusSession
from .serializers import FocusSessionSerializer
from .services import FocusSessionService

class FocusSessionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FocusSessionSerializer

    def get_queryset(self):
        return FocusSession.objects.filter(user=self.request.user)

    @decorators.action(detail=False, methods=['post'])
    def start(self, request):
        task_id = request.data.get('task')
        target_duration = request.data.get('target_duration')
        context = request.data.get('context')

        session = FocusSessionService.start_session(
            user=request.user,
            task_id=task_id,
            target_duration=target_duration,
            context=context
        )

        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=['patch'])
    def stop(self, request, pk=None):
        session = FocusSessionService.stop_session(user=request.user, session_id=pk)
        serializer = self.get_serializer(session)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=['patch'])
    def pause(self, request, pk=None):
        session = FocusSessionService.pause_session(user=request.user, session_id=pk)
        serializer = self.get_serializer(session)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=['patch'])
    def resume(self, request, pk=None):
        session = FocusSessionService.resume_session(user=request.user, session_id=pk)
        serializer = self.get_serializer(session)
        return Response(serializer.data)
