import datetime
from typing import List

from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import SAFE_METHODS, BasePermission


def get_patient_id_list_from_session(request) -> List:
    try:
        return request.session[settings.DOCTOR_SESSION_KEY].keys()
    except KeyError:
        return []


def check_patient_id_in_session(request, patient_id) -> bool:
    try:
        session_dct = request.session[settings.DOCTOR_SESSION_KEY]
    except KeyError:
        return False

    try:
        validity = datetime.datetime.fromisoformat(session_dct.get(str(patient_id), None))
    except (ValueError, TypeError):
        validity = None

    if validity is not None and validity > timezone.now():
        return True
    return False


def is_doctor(request) -> bool:
    return request.session.get(settings.DOCTOR_SESSION_KEY, None) is not None


class HasCompanyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.company is not None


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)


class IsOwnerOrObjIDInSession(BasePermission):

    def has_object_permission(self, request, view, obj):
        if check_patient_id_in_session(request, obj.id):
            return True
        return obj.is_owner(request.user)


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.has_admin_role()

    def has_object_permission(self, request, view, obj):
        return request.user.has_admin_role()


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.has_admin_role():
            return True
        if request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.has_admin_role():
            return True
        if request.method in SAFE_METHODS:
            return True
        return False


class IsCraOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.has_cra_role() or request.user.has_admin_role()

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return request.user.has_cra_role() or request.user.has_admin_role()


class IsCraOrAdminOrDoctor(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return is_doctor(request)
        return request.user.has_cra_role() or request.user.has_admin_role()

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return is_doctor(request)
        return request.user.has_cra_role() or request.user.has_admin_role()


class StudyStatusPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        from main.apps.studies import utils
        if request.method == 'DELETE':
            return utils.can_be_deleted(obj)
        if request.method in ['PUT', 'PATCH']:
            return utils.can_be_edit(obj)
        return True


class OnlyAdminCanCreatePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.has_admin_role()
        return True


class OnlyAdminOrCraCanCreatePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        if request.user.is_anonymous:
            return False
        return request.user.has_admin_role() or request.user.has_cra_role()


class OnlyAdminOrCraCanDeletePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method != 'DELETE':
            return True

        if request.user.is_anonymous:
            return False
        return request.user.has_admin_role() or request.user.has_cra_role()


class OnlyAdminOrCraCanListPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method != 'GET' or view.action == 'retrieve':
            return True

        if request.user.is_anonymous:
            return False
        return request.user.has_admin_role() or request.user.has_cra_role()


class OnlyAdminOrCraCanUpdatePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method not in ['PUT', 'PATCH']:
            return True

        if request.user.is_anonymous:
            return False
        return request.user.has_admin_role() or request.user.has_cra_role()


class OnlyAdminOrCraCanRetrievePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method != 'GET' or view.action == 'list':
            return True

        if request.user.is_anonymous:
            return False
        return request.user.has_admin_role() or request.user.has_cra_role()
