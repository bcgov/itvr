from rest_framework.viewsets import ModelViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny

from api.serializers.application_form import ApplicationFormSerializer, ApplicationFormCreateSerializer
from api.models.income_verification import IncomeVerification


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ApplicationFormViewset(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = IncomeVerification.objects.all()
    serializer_class = ApplicationFormSerializer

    serializer_classes = {
        'default': ApplicationFormSerializer,
        'create': ApplicationFormCreateSerializer,

    }

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get('default')
