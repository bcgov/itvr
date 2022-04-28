from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.models.household_member import HouseholdMember

from api.serializers.household_member import (
    HouseholdMemberApplicationGetSerializer,
    HouseholdMemberApplicationCreateSerializer,
)
from api.models.go_electric_rebate_application import GoElectricRebateApplication


class HouseholdMemberApplicationViewset(ModelViewSet):
    queryset = HouseholdMember.objects.all()
    serializer_classes = {
        "default": HouseholdMemberApplicationGetSerializer,
        "create": HouseholdMemberApplicationCreateSerializer,
    }

    @action(detail=True, methods=["GET"], url_path="initiate")
    def initiate(self, request, pk=None):
        application = GoElectricRebateApplication.objects.get(id=pk)
        household_member = HouseholdMember(application=application)
        serializer = HouseholdMemberApplicationGetSerializer(household_member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get("default")
