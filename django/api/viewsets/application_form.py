from rest_framework.viewsets import ModelViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from api.serializers.application_form import ApplicationFormSerializer, ApplicationFormSaveSerializer
from api.models.income_verification import IncomeVerification


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ApplicationFormViewset(ModelViewSet):
    permission_classes = []
    queryset = IncomeVerification.objects.all()
    serializer_class = ApplicationFormSerializer

    def create(self, request):
        serializer = ApplicationFormSaveSerializer(data=request.data,
                                                   context={'request': request}
                                                   )
        if serializer.is_valid():
            # Account.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Account could not be created with received data'
        }, status=status.HTTP_400_BAD_REQUEST)
