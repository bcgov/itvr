from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.serializers.application_form import (
    ApplicationFormSerializer,
    ApplicationFormCreateSerializer,
)
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from api.models.household_member import HouseholdMember
from api.serializers.household_member import HouseholdMemberApplicationGetSerializer


class ApplicationFormViewset(ModelViewSet):
    queryset = GoElectricRebateApplication.objects.all()
    serializer_classes = {
        "default": ApplicationFormSerializer,
        "create": ApplicationFormCreateSerializer,
    }

    @action(detail=True, methods=["GET"], url_path="household")
    def household(self, request, pk=None):
        household_member = HouseholdMember.objects.filter(application=pk)
        serializer = HouseholdMemberApplicationGetSerializer(
            household_member, many=True
        )
        return Response(serializer.data[0], status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get("default")
