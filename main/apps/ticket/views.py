from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from main.libraries.permissions import IsCraOrAdmin
from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSets(mixins.CreateModelMixin, GenericViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsCraOrAdmin]
