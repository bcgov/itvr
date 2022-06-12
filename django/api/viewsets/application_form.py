from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin

from api.serializers.application_form import (
    ApplicationFormSerializer,
    ApplicationFormCreateSerializer,
    ApplicationFormSpouseSerializer,
)
from api.models.go_electric_rebate_application import GoElectricRebateApplication


class ApplicationFormViewset(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = GoElectricRebateApplication.objects.all()
    serializer_classes = {
        "default": ApplicationFormSerializer,
        "create": ApplicationFormCreateSerializer,
    }

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
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get("default")

    @action(detail=False, methods=["GET"], url_path="check_status")
    def check_status(self, request, pk=None):
        drivers_license = request.query_params.get("drivers_license", None)
        application_status = GoElectricRebateApplication.objects.filter(
            drivers_licence=drivers_license
        ).values_list("status", flat=True)

        if application_status:
            if application_status[0] in [
                "submitted",
                "verified",
                "approved",
                "redeemed",
            ]:
                return Response({"validation": "fail"})
            elif application_status[0] in ["declined", "cra_error"]:
                return Response({"validation": "pass"})
        return Response({"validation": "pass"})
