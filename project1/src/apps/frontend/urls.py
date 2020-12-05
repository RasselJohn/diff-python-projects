from django.urls import path

from src.apps.frontend.permissions import user_only_request, staff_only_request
from src.apps.frontend.views import auth, user, IndexView

urlpatterns = [
    path(r'', IndexView.as_view(), name='index'),

    path(r'login/', auth.LoginView.as_view(), name='login'),
    path(r'logout/', auth.LogoutView.as_view(), name='logout'),

    path(r'users/', user_only_request(user.UserListView.as_view()), name='users'),
    path(r'user/add/', staff_only_request(user.UserAddView.as_view()), name='user_add'),
    path(r'user/edit/<str:user_id>/', staff_only_request(user.UserEditView.as_view()), name='user_edit'),
    path(r'user/remove/<str:user_id>/', staff_only_request(user.UserRemoveView.as_view()), name='user_remove'),
]
