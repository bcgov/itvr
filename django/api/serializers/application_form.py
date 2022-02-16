from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models.income_verification import IncomeVerification

class ApplicationFormCreateSerializer(ModelSerializer):
    class Meta:
        model = IncomeVerification
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        details = request.data.get('details')
        obj = IncomeVerification.objects.create(
            sin=details.get('sin'),
            last_name=details.get('last_name'),
            first_name=details.get('first_name'),
            date_of_birth=details.get('dob'),
            tax_year=details.get('tax_year'),            
        )
        return obj


class ApplicationFormSerializer(ModelSerializer):
    class Meta:
        model = IncomeVerification
        fields = '__all__'