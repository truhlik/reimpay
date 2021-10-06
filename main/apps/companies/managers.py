from django.db import models


class CompanyQuerySet(models.QuerySet):

    def prefetch_list(self):
        return self.prefetch_related('users')

    def owner(self, user):
        """ Vrátí company ve kterých je daný user vlastníkem. """
        if user.has_admin_role():
            return self.filter(users=user)
        return self.none()

    def full_text_search(self, term):
        """ Vrátí všechny company, které odpovídají danému query. """
        return self.filter(name__unaccent__icontains=term)

    def company(self, user):
        return self.filter(users=user)
