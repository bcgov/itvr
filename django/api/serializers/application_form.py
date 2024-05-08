from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from rest_framework.parsers import FormParser, MultiPartParser
from datetime import date
from rest_framework.response import Response
from rest_framework import status
from api.services.go_electric_rebate_application import equivalent_drivers_licence_number_found
from rest_framework.serializers import ValidationError


class ApplicationFormCreateSerializer(ModelSerializer):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    class Meta:
        model = GoElectricRebateApplication
        exclude = ["user", "status", "tax_year", "is_legacy"]

    def _get_tax_year(self):
        today = date.today()
        month = today.month
        year = today.year
        if month < 7:
            return year - 2
        return year - 1
    
    def validate_drivers_licence(self, value):
        if equivalent_drivers_licence_number_found(value):
            raise ValidationError("Equivalent DL# exists.")
        return value


class ApplicationFormCreateSerializerDefault(ApplicationFormCreateSerializer):
    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        obj = GoElectricRebateApplication.objects.create(
            sin=validated_data["sin"],
            status= GoElectricRebateApplication.Status.SUBMITTED,
            email=validated_data["email"],
            drivers_licence=validated_data["drivers_licence"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            middle_names=validated_data["middle_names"],
            date_of_birth=validated_data["date_of_birth"],
            address=validated_data["address"],
            city=validated_data["city"],
            postal_code=validated_data["postal_code"],
            doc1=validated_data["doc1"],
            doc2=validated_data["doc2"],
            tax_year=self._get_tax_year(),
            application_type=validated_data["application_type"],
            user=user,
            consent_personal=validated_data["consent_personal"],
            consent_tax=validated_data["consent_tax"],
        )
        return obj

class ApplicationFormCreateSerializerBCSC(ApplicationFormCreateSerializer):
    class Meta(ApplicationFormCreateSerializer.Meta):
        exclude = [
            "last_name",
            "first_name",
            "middle_names",
            "date_of_birth",
            "address",
            "city",
            "postal_code",
            "doc1",
            "doc2",
        ] + ApplicationFormCreateSerializer.Meta.exclude

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        try:
            obj = GoElectricRebateApplication.objects.create(
                sin=validated_data["sin"],
                status=GoElectricRebateApplication.Status.VERIFIED,
                email=validated_data["email"],
                drivers_licence=validated_data["drivers_licence"],
                last_name=user.last_name,
                first_name=user.first_name,
                date_of_birth=user.date_of_birth,
                address=user.street_address,
                city=user.locality,
                postal_code=user.postal_code,
                tax_year=self._get_tax_year(),
                application_type=validated_data["application_type"],
                user=user,
                consent_personal=validated_data["consent_personal"],
                consent_tax=validated_data["consent_tax"],
            )
            return obj
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationFormSerializer(ModelSerializer):
    sin = SerializerMethodField()

    def get_sin(self, obj):
        return "******" + str(obj.sin)[-3:]

    class Meta:
        model = GoElectricRebateApplication
        fields = (
            "id",
            "application_type",
            "status",
            "address",
            "city",
            "postal_code",
            "tax_year",
            "first_name",
            "middle_names",
            "last_name",
            "sin",
            "date_of_birth",
            "consent_personal",
            "consent_tax",
            "created",
            "email",
            "drivers_licence",
        )