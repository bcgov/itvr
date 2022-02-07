"""
Further reading:
https://www.django-rest-framework.org/api-guide/serializers/
"""
from rest_framework.serializers import ModelSerializer

from api.models.income_verification import IncomeVerification


class RushingStatsSerializer(ModelSerializer):
    """
    Default Serializer for Rushing Stats
    """

    class Meta:
        model = IncomeVerification
        fields = '__all__'