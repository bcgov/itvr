from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from api.serializers.application_form import (
    ApplicationFormSerializer,
    ApplicationFormCreateSerializerDefault,
    ApplicationFormCreateSerializerBCSC,
)
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from api.services.go_electric_rebate_application import equivalent_drivers_licence_number_found


class ApplicationFormViewset(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
):
    queryset = GoElectricRebateApplication.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            if self.request.user.identity_provider == "bcsc":
                return ApplicationFormCreateSerializerBCSC
            return ApplicationFormCreateSerializerDefault
        return ApplicationFormSerializer

    def retrieve(self, request, pk=None):
        application = GoElectricRebateApplication.objects.get(pk=pk)
        if application.user.id == request.user.id:
            serializer = ApplicationFormSerializer(application)
            return Response(serializer.data)
        response = {"message": "Forbidden"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)


    @action(detail=False, methods=["GET"], url_path="check_status")
    def check_status(self, request, pk=None):
        drivers_licence = request.query_params.get("drivers_license", None)
        dl_not_valid = equivalent_drivers_licence_number_found(drivers_licence)

        if dl_not_valid:
            return Response({"drivers_license_valid": "false"})
        return Response({"drivers_license_valid": "true"})

    @action(detail=False, methods=["GET"], url_path="check_accessible")
    def check_accessible(self, request, pk=None):
        return Response(status=status.HTTP_200_OK)
