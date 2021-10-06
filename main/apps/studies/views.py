from django.utils.decorators import method_decorator
from django.views.generic.detail import SingleObjectMixin
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from main.apps.core.swagger import path_id_param_str, path_id_param_int
from main.libraries import permissions
from main.libraries.serializers.mixins import GetSerializerClassMixin
from . import models, serializers, utils
from .filters import PatientVisitItemFilter, PatientFilter
from ...libraries.permissions import is_doctor, check_patient_id_in_session, get_patient_id_list_from_session
from ...libraries.views import ApiPdfTemplateView


@method_decorator(name='retrieve', decorator=path_id_param_str)
@method_decorator(name='update', decorator=path_id_param_str)
@method_decorator(name='partial_update', decorator=path_id_param_str)
@method_decorator(name='destroy', decorator=path_id_param_str)
@method_decorator(name='config', decorator=path_id_param_str)
class StudyViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = models.Study.objects.active().prefetch_related()
    permission_classes = [permissions.HasCompanyPermission, permissions.IsOwner, permissions.IsAdminOrReadOnly, permissions.StudyStatusPermission]
    filterset_fields = ['id']
    serializer_class = serializers.StudyReadSerializer
    suffix = 'List'
    serializer_action_classes = {
        'list': serializers.StudyReadSerializer,
        'retrieve': serializers.StudyReadSerializer,
        'update': serializers.StudyWriteSerializer,
        'partial_update': serializers.StudyWriteSerializer,
        'create': serializers.StudyWriteSerializer,
        'config': serializers.StudyConfigSerializer,
        'users': serializers.UserSerializer,
    }

    def get_queryset(self):
        qs = super(StudyViewSet, self).get_queryset().list(self.request.user).order_by('identifier')
        if self.action == 'list':
            qs = qs.prefetch_list()
        return qs

    def perform_destroy(self, instance):
        instance.custom_delete()

    @action(methods=['GET'], detail=True, serializer_class=serializers.StudyConfigSerializer)
    def config(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk == 'null':
            instance = models.Study()
        else:
            instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @property
    def paginator(self):
        if self.action == 'users':
            return None
        return super(StudyViewSet, self).paginator


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class StudyItemViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = models.StudyItem.objects.all()
    permission_classes = [permissions.HasCompanyPermission, permissions.IsOwner, permissions.IsAdmin,
                          permissions.StudyStatusPermission]
    serializer_class = serializers.StudyItemSerializer
    filterset_fields = ['study_id']

    def get_queryset(self):
        return super(StudyItemViewSet, self).get_queryset().company(self.request.user)

    def perform_destroy(self, instance):
        instance.custom_delete()


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class ArmViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = models.Arm.objects.all()
    permission_classes = [permissions.HasCompanyPermission, permissions.IsOwner, permissions.IsAdminOrReadOnly,
                          permissions.StudyStatusPermission]
    serializer_class = serializers.ArmSerializer
    filterset_fields = ['study_id']

    def get_queryset(self):
        return super(ArmViewSet, self).get_queryset().company(self.request.user)

    def perform_destroy(self, instance):
        instance.custom_delete()


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class SiteViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = models.Site.objects.active()
    permission_classes = [permissions.HasCompanyPermission, permissions.IsOwner, permissions.IsAdminOrReadOnly,
                          permissions.StudyStatusPermission]
    serializer_class = serializers.SiteSerializer
    serializer_action_classes = {
        'retrieve': serializers.SiteSerializer,
        'create': serializers.SiteSerializer,
        'update': serializers.SiteSerializer,
        'partial_update': serializers.SiteSerializer,
        'destroy': serializers.SiteSerializer,
        'list': serializers.SiteSerializer,
        'patients': serializers.SitePatientSerializer,
    }
    filterset_fields = ['study_id', 'id']

    def get_queryset(self):
        return super(SiteViewSet, self).get_queryset().company(self.request.user).order_by('title')

    @action(methods=['GET'], detail=False, serializer_class=serializers.SitePatientSerializer)
    def patients(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.custom_delete()


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
# @method_decorator(name='destroy', decorator=path_id_param_int)
class PatientViewSet(GetSerializerClassMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = models.Patient.objects.all().select_related('arm', 'site').prefetch_related('patient_visits')
    permission_classes = [permissions.IsCraOrAdminOrDoctor,
                          permissions.OnlyAdminOrCraCanCreatePermission,
                          permissions.OnlyAdminOrCraCanDeletePermission,
                          permissions.OnlyAdminOrCraCanListPermission,
                          permissions.IsOwnerOrObjIDInSession,
                          permissions.StudyStatusPermission,
                          ]
    serializer_class = serializers.PatientBaseSerializer
    serializer_action_classes = {
        'retrieve': serializers.PatientDetailSerializer
    }
    # filterset_fields = ['study_id', 'site_id']
    filter_class = PatientFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = super(PatientViewSet, self).get_queryset().company(self.request.user)
        elif is_doctor(self.request):
            patient_id_lst = get_patient_id_list_from_session(self.request)
            qs = super(PatientViewSet, self).get_queryset().filter(id__in=patient_id_lst)
        else:
            return super(PatientViewSet, self).get_queryset().none()
        if self.action == 'retrieve':
            qs = qs.prefetch_detail()
        return qs


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class VisitViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = models.Visit.objects.all().select_related('arm', 'study')
    permission_classes = [permissions.HasCompanyPermission, permissions.IsOwner, permissions.IsAdminOrReadOnly,
                          permissions.StudyStatusPermission]
    serializer_class = serializers.VisitSerializer
    filterset_fields = ['study_id', 'arm_id']

    def get_queryset(self):
        return super(VisitViewSet, self).get_queryset().active().company(self.request.user).order_by('order')

    def perform_destroy(self, instance):
        instance.custom_delete()


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class VisitItemViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = models.VisitItem.objects.all().active()
    permission_classes = [permissions.HasCompanyPermission, permissions.IsOwner, permissions.IsAdminOrReadOnly,
                          permissions.StudyStatusPermission]
    serializer_class = serializers.VisitItemSerializer
    filterset_fields = ['visit_id']

    def get_queryset(self):
        return super(VisitItemViewSet, self).get_queryset().active().company(self.request.user)

    def perform_destroy(self, instance):
        instance.custom_delete()


@method_decorator(name='destroy', decorator=path_id_param_int)
class PatientVisitViewSet(GetSerializerClassMixin,
                          mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = models.PatientVisit.objects.all()
    permission_classes = [permissions.IsCraOrAdminOrDoctor,
                          permissions.OnlyAdminOrCraCanDeletePermission,
                          permissions.OnlyAdminOrCraCanUpdatePermission,
                          permissions.StudyStatusPermission,
                          ]
    serializer_class = serializers.PatientVisitSerializer
    filterset_fields = ['patient_id']

    def get_queryset(self):

        if self.request.user.is_authenticated:
            return super(PatientVisitViewSet, self).get_queryset().company(self.request.user)

        elif is_doctor(self.request):
            patient_id = self.request.GET.get('patient_id', None)
            if not check_patient_id_in_session(self.request, patient_id):
                return super(PatientVisitViewSet, self).get_queryset().none()
            return super(PatientVisitViewSet, self).get_queryset().filter(patient_id=patient_id)

        return super(PatientVisitViewSet, self).get_queryset().none()

    def perform_destroy(self, instance):
        if not utils.can_delete_patient_visit(instance):
            raise ValidationError("You are not allowed to perform this action.")
        instance.delete()


@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
class PatientVisitItemViewSet(GetSerializerClassMixin,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):

    queryset = models.PatientVisitItem.objects.all().select_related('patient_visit__patient', 'visit_item')
    permission_classes = [permissions.IsCraOrAdminOrDoctor,
                          permissions.OnlyAdminOrCraCanCreatePermission,
                          permissions.OnlyAdminOrCraCanDeletePermission,
                          permissions.OnlyAdminOrCraCanUpdatePermission,
                          permissions.IsOwner,
                          permissions.StudyStatusPermission,
                          ]
    serializer_class = serializers.PatientVisitItemSerializer
    filter_class = PatientVisitItemFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super(PatientVisitItemViewSet, self).get_queryset().owner(self.request.user)

        elif is_doctor(self.request):
            patient_id = self.request.GET.get('patient_id', None)
            if not check_patient_id_in_session(self.request, patient_id):
                return super(PatientVisitItemViewSet, self).get_queryset().none()
            return super(PatientVisitItemViewSet, self).get_queryset().filter(patient_id=patient_id)

        return super(PatientVisitItemViewSet, self).get_queryset().none()


class SitesInstructionPDFView(SingleObjectMixin, ApiPdfTemplateView):
    permission_classes = [permissions.IsCraOrAdmin]
    filename = 'site_instruction.pdf'
    template_name = 'sites/instrukce.html'
    cmd_options = {
        'margin-top': 3,
    }

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return models.Site.objects.none()
        return models.Site.objects.owner(self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SitesInstructionPDFView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(SitesInstructionPDFView, self).get_context_data(**kwargs)
        ctx.update({
            'site': self.object,
            'study': self.object.study,
        })
        return ctx


class SitesPatientFormPDFView(SingleObjectMixin, ApiPdfTemplateView):
    permission_classes = [permissions.IsCraOrAdmin]
    filename = 'patient_form.pdf'
    template_name = 'sites/souhlas.html'
    cmd_options = {
        'margin-top': 20,
    }

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return models.Site.objects.none()
        return models.Site.objects.owner(self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SitesPatientFormPDFView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(SitesPatientFormPDFView, self).get_context_data(**kwargs)
        ctx.update({
            'site': self.object,
            'study': self.object.study,
            'sponsor_name': self.object.study.get_sponsor_name(),
            'cro': self.object.study.is_cro_operator(),
        })
        return ctx
