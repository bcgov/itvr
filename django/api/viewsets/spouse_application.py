from rest_framework.viewsets import ModelViewSet
from api.serializers.spouse_application import (
    SpouseApplicationSerializer,
    SpouseApplicationCreateSerializer,
)
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from api.models.household_member import HouseholdMember


class SpouseApplicationViewset(ModelViewSet):
    queryset = GoElectricRebateApplication.objects.all()
    serializer_classes = {
        "default": SpouseApplicationSerializer,
        "create": SpouseApplicationCreateSerializer,
    }

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get("default")
