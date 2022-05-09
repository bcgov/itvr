from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin

from api.models.household_member import HouseholdMember

from api.serializers.household_member import (
    HouseholdMemberApplicationGetSerializer,
    HouseholdMemberApplicationCreateSerializer,
)


class HouseholdMemberApplicationViewset(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin
):
    queryset = HouseholdMember.objects.all()
    serializer_classes = {
        "default": HouseholdMemberApplicationGetSerializer,
        "create": HouseholdMemberApplicationCreateSerializer,
    }

    def retrieve(self, request, pk=None):
        household_member = HouseholdMember.objects.get(application=pk)
        if household_member.user.id == request.user.id:
            serializer = HouseholdMemberApplicationGetSerializer(household_member)
            return Response(serializer.data)
        response = {"message": "Forbidden"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get("default")
