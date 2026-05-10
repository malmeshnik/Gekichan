from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, ProjectMemberViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'members', ProjectMemberViewSet, basename='project-members')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
]
