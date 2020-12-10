from django.urls import path
from src.apps.api import views

urlpatterns = [
    path(r'visited-links/', views.DomainsAddView.as_view(), name='visited-links'),
    path(r'visited-domains/', views.DomainsListView.as_view(), name='visited-domains'),
]
