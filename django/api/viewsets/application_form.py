from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.decorators import action

from api.serializers.application_form import ApplicationFormSerializer, ApplicationFormSaveSerializer
from api.models.income_verification import IncomeVerification


class ApplicationFormViewset(GenericViewSet, ListModelMixin):
    """
    This will build the list view and tie it with the serializer and
    permissions
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'put']

    serializer_classes = {
        'default': ApplicationFormSerializer,
    }
    @action(detail=False, methods=['post'])
    def create_application(self, request):
        print('TEST!!!')
        return Response('success!', status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = IncomeVerification.objects.all()

        return queryset

    def get_serializer_class(self):
        if self.action in list(self.serializer_classes.keys()):
            return self.serializer_classes.get(self.action)

        return self.serializer_classes.get('default')