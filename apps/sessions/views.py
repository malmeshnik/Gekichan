from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from .models import FocusSession
from .serializers import FocusSessionSerializer
from .services import start_focus_session, stop_focus_session, pause_focus_session

class FocusSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for FocusSession.
    Note: We use ReadOnlyModelViewSet to provide list/retrieve,
    but use custom actions for lifecycle management.
    """
    serializer_class = FocusSessionSerializer

    def get_queryset(self):
        return FocusSession.objects.filter(user=self.request.user)

    @decorators.action(detail=False, methods=['post'])
    def start(self, request):
        task_id = request.data.get('task')
        context = request.data.get('context')

        session = start_focus_session(
            user=request.user,
            task_id=task_id,
            context=context
        )

        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=['patch'])
    def stop(self, request, pk=None):
        session = stop_focus_session(user=request.user, session_id=pk)
        serializer = self.get_serializer(session)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=['patch'])
    def pause(self, request, pk=None):
        session = pause_focus_session(user=request.user, session_id=pk)
        serializer = self.get_serializer(session)
        return Response(serializer.data)
