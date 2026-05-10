from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, AttachmentViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'attachments', AttachmentViewSet, basename='attachment')

urlpatterns = [
    path('', include(router.urls)),
]
