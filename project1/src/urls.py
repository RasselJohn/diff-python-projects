from django.urls import path, include

urlpatterns = [
    path(r'', include('src.apps.frontend.urls')),
]
