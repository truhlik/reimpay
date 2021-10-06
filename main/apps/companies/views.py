from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed

from main.apps.core.swagger import path_id_param_int
from main.libraries import permissions
from . import models, serializers


@method_decorator(name='retrieve', decorator=path_id_param_int)
class CompanyViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    Viewsets pro Company se týká vždy objektů patřících danému uživateli,
    takže je dovoleno provádět update, delete apod.
    """

    queryset = models.Company.objects.all().prefetch_list()
    serializer_class = serializers.BaseCompanySerializer
    permission_classes = [permissions.HasCompanyPermission, permissions.IsOwner, permissions.IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'tags__name', 'categories__name']

    def get_queryset(self):
        return super(CompanyViewSet, self).get_queryset().company(self.request.user)

    @action(methods=['get', 'put', 'patch'], detail=False)
    def primary(self, request, *args, **kwargs):
        primary_company = self.get_queryset().first()
        if primary_company is None:
            raise Http404

        self.kwargs.update({'pk': primary_company.id})
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'PATCH':
            raise MethodNotAllowed('PATCH')
        else:
            raise NotImplementedError()
