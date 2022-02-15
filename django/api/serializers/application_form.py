from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models.income_verification import IncomeVerification

class ApplicationFormCreateSerializer(ModelSerializer):
    class Meta:
        model = IncomeVerification
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        print(request)
        obj = IncomeVerification.objects.create(
            sin=request.data.get('sin'),
            last_name=request.data.get('last_name'),
            first_name=request.data.get('first_name'),
            date_of_birth=request.data.get('dob'),
            tax_year=request.data.get('tax_year'),

        )

        return obj


class ApplicationFormSerializer(ModelSerializer):
    class Meta:
        model = IncomeVerification
        fields = '__all__'