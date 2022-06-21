from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin

from api.serializers.application_form import (
    ApplicationFormSerializer,
    ApplicationFormCreateSerializerDefault,
    ApplicationFormCreateSerializerBCSC,
    ApplicationFormSpouseSerializer,
)
from api.models.go_electric_rebate_application import GoElectricRebateApplication


class ApplicationFormViewset(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = GoElectricRebateApplication.objects.all()

    @action(detail=True, methods=["GET"], url_path="household")
    def household(self, request, pk=None):
        # not possible to restrict this endpoint to only the spouse because, at this point,
        # no household_member record associated with the spouse has been created yet, and we're not storing the spouse email
        # associated with household applications
        application = GoElectricRebateApplication.objects.get(pk=pk)
        serializer = ApplicationFormSpouseSerializer(application)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        application = GoElectricRebateApplication.objects.get(pk=pk)
        if application.user.id == request.user.id:
            serializer = ApplicationFormSerializer(application)
            return Response(serializer.data)
        response = {"message": "Forbidden"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def get_serializer_class(self):
        if self.action == "create":
            if self.request.user.identity_provider == "bcsc":
                return ApplicationFormCreateSerializerBCSC
            return ApplicationFormCreateSerializerDefault
        return ApplicationFormSerializer

    @action(detail=False, methods=["GET"], url_path="check_status")
    def check_status(self, request, pk=None):
        drivers_licence = request.query_params.get("drivers_license", None)
        dl_not_valid = (
            GoElectricRebateApplication.objects.filter(
                drivers_licence__exact=drivers_licence
            )
            .filter(
                status__in=[
                    GoElectricRebateApplication.Status.SUBMITTED,
                    GoElectricRebateApplication.Status.HOUSEHOLD_INITIATED,
                    GoElectricRebateApplication.Status.VERIFIED,
                    GoElectricRebateApplication.Status.APPROVED,
                    GoElectricRebateApplication.Status.REDEEMED,
                ]
            )
            .exists()
        )

        if dl_not_valid:
            return Response({"drivers_license_valid": "false"})
        return Response({"drivers_license_valid": "true"})
