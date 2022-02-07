"""
Viewset for Rushing stats
"""
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from api.serializers.rushing_stats import RushingStatsSerializer
from api.models.income_verification import IncomeVerification


class RushingStatsViewset(GenericViewSet, ListModelMixin):
    """
    This will build the list view and tie it with the serializer and
    permissions
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    serializer_classes = {
        'default': RushingStatsSerializer
    }

    def get_queryset(self):
        queryset = IncomeVerification.objects.all()

        return queryset

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get('default')