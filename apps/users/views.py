from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class TelegramAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return Response(
            {"detail": "Telegram auth logic not implemented yet."},
            status=status.HTTP_200_OK
        )
