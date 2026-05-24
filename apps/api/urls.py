from django.urls import path, include

urlpatterns = [
    path('', include('apps.users.urls')),
    path('', include('apps.projects.urls')),
    path('', include('apps.tasks.urls')),
    path('', include('apps.sessions.urls')),
    path('analytics/', include('apps.analytics.urls')),
]
