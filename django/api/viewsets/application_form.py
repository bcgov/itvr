from rest_framework.viewsets import ModelViewSet
from api.serializers.application_form import ApplicationFormSerializer, \
    ApplicationFormCreateSerializer
from api.models.go_electric_rebate_application import GoElectricRebateApplication


class ApplicationFormViewset(ModelViewSet):
    queryset = GoElectricRebateApplication.objects.all()
    serializer_classes = {
        'default': ApplicationFormSerializer,
        'create': ApplicationFormCreateSerializer,
    }

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get('default')
