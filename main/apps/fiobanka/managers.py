from django.db import models


class FiobankTransactionsQuerySet(models.QuerySet):

    def for_processing(self):
        """ Vrátí všechny platby, které by se měly zprocesovat. """
        return self.filter(processed_on__isnull=True,
                           amount__gte=0,
                           variable_symbol__isnull=False)\
            .exclude(variable_symbol='')

    def not_processed_yet(self):
        return self.filter(processed_on__isnull=True)
