from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='public/index.html'), name='index'),
    path(r'admin/', TemplateView.as_view(template_name='public/admin.html'), name='admin'),
]
