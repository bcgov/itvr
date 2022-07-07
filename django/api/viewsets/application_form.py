from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from api.serializers.application_form import (
    ApplicationFormSerializer,
    ApplicationFormCreateSerializerDefault,
    ApplicationFormCreateSerializerBCSC,
    ApplicationFormSpouseSerializer,
)
from api.models.go_electric_rebate_application import GoElectricRebateApplication


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

    # currently only used for cancelling household_initiated applications; consider using a serializer if the logic becomes more complicated
    def partial_update(self, request, pk=None):
        if request.data.get("status") == GoElectricRebateApplication.Status.CANCELLED:
            application = GoElectricRebateApplication.objects.get(pk=pk)
            if (
                application.status
                == GoElectricRebateApplication.Status.HOUSEHOLD_INITIATED
            ):
                application.status = GoElectricRebateApplication.Status.CANCELLED
                application.save(update_fields=["status"])
                return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path="household")
    def household(self, request, pk=None):
        application = GoElectricRebateApplication.objects.get(pk=pk)
        if application.status == GoElectricRebateApplication.Status.CANCELLED:
            error = {"error": "application_cancelled"}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        application_user_id = application.user.id
        household_user_id = request.user.id
        if application_user_id == household_user_id:
            error = {"error": "same_user"}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ApplicationFormSpouseSerializer(application)
        return Response(serializer.data)

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
