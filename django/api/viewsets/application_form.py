from rest_framework.viewsets import ModelViewSet
from api.serializers.application_form import ApplicationFormSerializer, \
    ApplicationFormCreateSerializer
from api.models.income_verification import IncomeVerification


class ApplicationFormViewset(ModelViewSet):
    queryset = IncomeVerification.objects.all()
    serializer_classes = {
        'default': ApplicationFormSerializer,
        'create': ApplicationFormCreateSerializer,
    }

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get('default')
