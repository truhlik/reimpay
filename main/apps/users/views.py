from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework import viewsets

from main.apps.core.swagger import path_id_param_str
from main.apps.users.utils import send_password_reset
from main.libraries import permissions
from .filters import UserStudyFilter
from .models import User
from .serializers import UserSerializer


@method_decorator(name='retrieve', decorator=path_id_param_str)
@method_decorator(name='update', decorator=path_id_param_str)
@method_decorator(name='partial_update', decorator=path_id_param_str)
@method_decorator(name='destroy', decorator=path_id_param_str)
class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.active()
    serializer_class = UserSerializer
    permission_classes = [permissions.HasCompanyPermission, permissions.IsOwner, permissions.IsCraOrAdmin,
                          permissions.OnlyAdminCanCreatePermission]
    filter_class = UserStudyFilter

    def get_queryset(self):
        return super(UserViewSets, self).get_queryset().owner(self.request.user)

    @action(methods=['get', 'patch', 'delete'], detail=False)
    def self(self, request, *args, **kwargs):
        self.kwargs.update({'pk': self.get_queryset().first().id})
        if request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, *args, **kwargs)
        else:
            return self.retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
        send_password_reset(self.request, serializer.data['email'])

    def perform_destroy(self, instance):
        instance.custom_delete()
