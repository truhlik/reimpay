from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users import constants as user_constatnts

from ... import constants
from ...utils import create_visits


class BaseViewPermissionTestCase(APITestCase):

    def setUp(self) -> None:
        super(BaseViewPermissionTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.c2 = baker.make('companies.Company')

        self.user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c1)
        self.user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c1)

        self.study1 = baker.make('studies.Study', company=self.c1, bank_transfer=True, post_office_cash=True)
        self.site1 = baker.make('studies.Site', study=self.study1, cra=self.user_cra)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        create_visits(self.study1, self.arm1)
        self.patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=self.site1, number='7998862/0800')
        self.visit1 = baker.make('studies.Visit', study=self.study1, arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1, price=100)
        self.visit_item = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1,
                                     study_item=self.study_item1)
        self.patient_visit = baker.make('studies.PatientVisit', patient=self.patient1, visit=self.visit1,
                                        study=self.study1, )

        self.pvi = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item)
