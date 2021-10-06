from .. import models
from .. import permissions

PERM_CLS = {
    models.PatientVisit: permissions.PatientVisitPermission,
    models.PatientVisitItem: permissions.PatientVisitItemPermission,
    models.Study: permissions.StudyPermission,
    models.Patient: permissions.PatientPermission,
}


def can_be_created(model, rel_obj):
    cls = PERM_CLS.get(model, permissions.StudyRelatedPermission)  # vytahnu si class
    return cls.can_be_created(rel_obj)


def can_be_edit(obj):
    cls = PERM_CLS.get(obj._meta.model, permissions.StudyRelatedPermission)  # vytahnu si class
    perm_cls = cls(obj)  # inicializuji classu
    return perm_cls.can_be_edit()


def can_be_deleted(obj):
    cls = PERM_CLS.get(obj._meta.model, permissions.StudyRelatedPermission)  # vytahnu si class
    perm_cls = cls(obj)  # inicializuji classu
    return perm_cls.can_be_deleted()
