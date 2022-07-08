from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from api.models.go_electric_rebate_application import GoElectricRebateApplication


# unrestricted viewset
class OpenApplicationFormViewset(GenericViewSet, UpdateModelMixin):
    queryset = GoElectricRebateApplication.objects.all()
    authentication_classes = []
    permission_classes = []

    @action(detail=True, methods=["GET"], url_path="cancellable")
    def get_cancellable(self, request, pk=None):
        cancellable = (
            GoElectricRebateApplication.objects.filter(pk=pk)
            .filter(status=GoElectricRebateApplication.Status.HOUSEHOLD_INITIATED)
            .exists()
        )
        if cancellable:
            return Response({"cancellable": True})
        return Response({"cancellable": False})

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
