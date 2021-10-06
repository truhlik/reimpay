from typing import Optional

from ..models import Study, PatientVisitItem
from .. import constants


class StudyStatusValidation(object):

    def __init__(self, study: Optional[Study]):
        self.study = study

    def _validate_status_draft(self):
        return True

    def _validate_status_prelaunch(self):
        if self.study is None:
            return False

        if not self.study.study_items.active().exists():
            return False

        return True

    def _validate_status_progress(self):
        if self.study is None:
            return False

        return True

    def _validate_status_billing(self):

        if self.study is None:
            return False

        # nelze přepnout studii do Billing, pokud má ještě nějaké neprocesované Reims
        if PatientVisitItem.objects.not_processed().for_study(self.study).exists():
            return False

        return True

    def _validate_status_closed(self):
        if self.study is None:
            return False

        return True

    @staticmethod
    def get_allowed_status_from_current(current_status):
        """ Vrátí statusy, na které je dovoleno změnit ze současného. """

        # allowed_change = {
        #     None: [constants.STUDY_STATUS_DRAFT],
        #     constants.STUDY_STATUS_DRAFT: [constants.STUDY_STATUS_PRELAUNCH],
        #     constants.STUDY_STATUS_PRELAUNCH: [constants.STUDY_STATUS_DRAFT],
        #     constants.STUDY_STATUS_PROGRESS: [constants.STUDY_STATUS_BILLING],
        #     constants.STUDY_STATUS_BILLING: [constants.STUDY_STATUS_CLOSED],
        #     constants.STUDY_STATUS_CLOSED: [],
        # }

        # uživatel může pouze přepnout na PRELAUNCH a BILLING ... zbytek je automatika
        allowed_change = {
            None: [constants.STUDY_STATUS_DRAFT],
            constants.STUDY_STATUS_DRAFT: [constants.STUDY_STATUS_PRELAUNCH],
            constants.STUDY_STATUS_PRELAUNCH: [constants.STUDY_STATUS_DRAFT],
            constants.STUDY_STATUS_PROGRESS: [constants.STUDY_STATUS_BILLING],
            constants.STUDY_STATUS_BILLING: [],
            constants.STUDY_STATUS_CLOSED: [],
        }
        return allowed_change[current_status]

    def can_change_status(self, new_status):
        original_status = self.study.status if self.study else None

        # pokud neudělám žádnou změnu, tak povol
        if original_status == new_status:
            return True

        allowed_statuses = StudyStatusValidation.get_allowed_status_from_current(original_status)

        if new_status not in allowed_statuses:
            return False

        return getattr(self, '_validate_status_{}'.format(new_status.lower()))()
