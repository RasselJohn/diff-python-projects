from django.urls import path, include

urlpatterns = [
    path('api/', include('src.apps.api.urls')),
]
