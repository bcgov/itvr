from rest_framework.viewsets import ModelViewSet
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from api.serializers.application_form import ApplicationFormSerializer, ApplicationFormSaveSerializer
from api.models.income_verification import IncomeVerification


class ApplicationFormViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IncomeVerification.objects.all()
    serializer_class = ApplicationFormSerializer

    @action(detail=False, methods=['post'])
    def create_application(self, request):
        serializer = ApplicationFormSaveSerializer(data=request.data,
                                                   context={'request': request}
                                                   )
        return Response('success!', status=status.HTTP_201_CREATED)
