from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StatsViewSet, ProductivityAnalyticsAPIView

router = DefaultRouter()
router.register(r"stats", StatsViewSet, basename="stats")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "projects/<uuid:project_id>/productivity/",
        ProductivityAnalyticsAPIView.as_view(),
        name="project-productivity"
    ),
    path(
        "productivity/",
        ProductivityAnalyticsAPIView.as_view(),
        name="global-productivity"
    ),
]
