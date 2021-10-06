from . import constants


class StudyRelatedPermission(object):
    create_lst = [
        constants.STUDY_STATUS_DRAFT, constants.STUDY_STATUS_PROGRESS
    ]
    edit_lst = [
        constants.STUDY_STATUS_DRAFT, constants.STUDY_STATUS_PROGRESS
    ]
    delete_lst = [
        constants.STUDY_STATUS_DRAFT, constants.STUDY_STATUS_PROGRESS
    ]

    def __init__(self, *args, **kwargs):
        self.obj = args[0]

    @classmethod
    def can_be_created(cls, study):
        return study.status in cls.create_lst if study is not None else False

    def can_be_edit(self):
        return self._get_rel_obj().status in self.edit_lst

    def can_be_deleted(self):
        return self._get_rel_obj().status in self.delete_lst

    def _get_rel_obj(self):
        return self.obj.study


class StudyPermission(StudyRelatedPermission):

    def _get_rel_obj(self):
        return self.obj


class PatientVisitPermission(StudyRelatedPermission):
    create_lst = [
        constants.STUDY_STATUS_PROGRESS
    ]


class PatientVisitItemPermission(StudyRelatedPermission):
    create_lst = [
        constants.STUDY_STATUS_PROGRESS
    ]
    edit_lst = [
        constants.STUDY_STATUS_PROGRESS
    ]

    def _get_rel_obj(self):
        return self.obj.visit_item.study


class PatientPermission(StudyRelatedPermission):
    create_lst = [
        constants.STUDY_STATUS_PROGRESS
    ]
    edit_lst = [
        constants.STUDY_STATUS_PROGRESS
    ]

