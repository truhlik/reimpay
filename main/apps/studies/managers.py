from django.db import models
from django.utils import timezone

from . import constants


class StudyQuerySet(models.QuerySet):

    def list(self, user):
        if user.is_anonymous:
            return self.none()
        if user.has_admin_role():
            return self.filter(company=user.company)
        else:
            return self.filter(sites__cra=user).distinct()

    def owner(self, user):
        """ Vrátí studie pro které je daný user vlastníkem. """
        if user.has_admin_role():
            return self.filter(company=user.company)
        return self.none()

    def company(self, user):
        """ Vrátí studie pro které je daný user přiřazen. """
        if user.is_anonymous:
            return self.none()
        return self.filter(company=user.company)

    def active(self):
        return self.filter(models.Q(closed_at__gte=timezone.now()) | models.Q(closed_at__isnull=True))

    def prefetch_list(self):
        return self.prefetch_related('patients')


class StudyRelatedQuerySet(models.QuerySet):

    def active(self):
        return self.filter(deleted=False)

    def company(self, user):
        """ Vrátí objekty pro tohoto uživatele"""
        if user.is_anonymous:
            return self.none()
        return self.filter(study__company=user.company)

    def owner(self, user):
        """ Vrátí objekty pro které je daný user vlastníkem. """
        if user.has_admin_role():
            return self.filter(study__company=user.company)
        return self.none()


class StudyItemQuerySet(StudyRelatedQuerySet):
    pass


class ArmQuerySet(StudyRelatedQuerySet):
    pass


class SiteQuerySet(StudyRelatedQuerySet):

    def owner(self, user):
        if user.has_admin_role():
            return self.filter(study__company=user.company)
        elif user.has_cra_role():
            return self.filter(cra=user)
        return self.none()


class PatientQuerySet(StudyRelatedQuerySet):

    def prefetch_detail(self):
        return self.prefetch_related('patient_visits__patient_visit_items__visit_item__study_item')

    def owner(self, user):
        if user.has_admin_role():
            # admin má práva na všechny pacienty v dané company
            return self.filter(study__company=user.company)
        # cra má práva jenom na pacienty, které jsou na jeho site
        return self.filter(site__cra=user)

    def flagged(self):
        return self.filter(change_payment_request__isnull=False)

    def not_flagged(self):
        return self.filter(change_payment_request__isnull=True)

    def in_progress(self):
        """ Vrátí pacienty, kteří ještě nejsou ukočení. """
        return self.filter(status=constants.STUDY_PATIENT_STATUS_ACTIVE)


class VisitQuerySet(StudyRelatedQuerySet):

    def scheduled(self):
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit_type__in=[constants.STUDY_VISIT_TYPE_DISCONTINUAL, constants.STUDY_VISIT_TYPE_REGULAR])

    def regular(self):
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit_type__in=[constants.STUDY_VISIT_TYPE_REGULAR])

    def unscheduled(self):
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit_type=constants.STUDY_VISIT_TYPE_UNSCHEDULED)

    def discontinual(self):
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL)

    def update_order(self, arm, old_order, new_order):
        if old_order == new_order:
            return

        qs = self.active().regular().filter(arm=arm)

        if old_order is None:
            # vytvářím nový objekt => musím posunout o +1 všechny následující
            return qs.filter(order__gte=new_order).update(order=models.F('order') + 1)
        elif new_order is None:
            # mažu objekt => musím posunout o -1 všechny následující
            return qs.filter(order__gt=old_order).update(order=models.F('order') - 1)
        elif new_order > old_order:
            # posouvám dolů => zvětšuju order, takže ostatním musím snížit
            return qs.filter(order__gt=old_order, order__lte=new_order).update(order=models.F('order') - 1)
        else:
            # posouvám nahoru (new_order < old_order) snižuju order, takže ostatním musím zvětšit
            return qs.filter(order__gte=new_order, order__lt=old_order).update(order=models.F('order') + 1)


class VisitItemQuerySet(StudyRelatedQuerySet):

    def regular(self):
        # todo need test
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit__visit_type__in=[constants.STUDY_VISIT_TYPE_REGULAR])

    def unscheduled(self):
        # todo need test
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit__visit_type=constants.STUDY_VISIT_TYPE_UNSCHEDULED)

    def discontinual(self):
        # todo need test
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit__visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL)


class PatientVisitQuerySet(StudyRelatedQuerySet):
    pass

    def discontinual(self):
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit__visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL)

    def regular(self):
        """ Vrátí visits, které jsou scheduled - regular a discountinual. """
        return self.filter(visit__visit_type=constants.STUDY_VISIT_TYPE_REGULAR)

    def owner(self, user):
        """ Vlastním ty PatientVisit, které jsou pacientů, které vlastním ===> kopíruje Pacient.objects.owner() """

        if user.has_admin_role():
            # admin má práva na všechny pacient visity v dané company
            return self.filter(patient__study__company=user.company)
        # cra má práva jenom na pacienty, které jsou na jeho site
        return self.filter(patient__site__cra=user)


class PatientVisitItemQuerySet(models.QuerySet):

    def approved(self):
        return self.filter(approved=True)

    def rejected(self):
        return self.filter(approved=False)

    def owner(self, user):
        if user.has_admin_role():
            # admin má práva na všechno v dané company
            return self.filter(patient_visit__patient__study__company=user.company)
        # cra má práva jenom na pacienty, které jsou na jeho site
        return self.filter(patient_visit__patient__site__cra=user)

    def company(self, user):
        """ Vrací objekty patřící spolenosti daného uživatele. """

        if user.is_anonymous:
            return self.none()
        return self.filter(patient_visit__patient__study__company=user.company)

    def get_reims_sum(self) -> int:
        return self.aggregate(sum=models.Sum('visit_item__study_item__price'))['sum']

    def not_processed(self):
        """ Vrátí ještě nezprocesované Reims. """
        return self.filter(approved=None)

    def for_study(self, study):
        """ Vrátí PVI pro tuto studii. """
        return self.filter(patient_visit__study=study)

    def processed(self):
        return self.exclude(approved=None)
