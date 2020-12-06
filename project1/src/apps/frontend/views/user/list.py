from django.contrib.auth.models import User
from django.db.models.query import RawQuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class UserListView(View):
    template_name = 'users.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        users: RawQuerySet = User.objects.raw(
            'SELECT * FROM auth_user WHERE is_active = TRUE AND id!= %s',
            [request.user.pk]
        )
        # ORM analog
        # User.objects.filter(is_active=True).exclude(pk=request.user.pk)

        return render(request, self.template_name, {'users_data': list(users)})
