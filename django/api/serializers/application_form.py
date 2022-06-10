from api.validators import validate_file_size
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from rest_framework.parsers import FormParser, MultiPartParser
from datetime import date
from django.core.exceptions import ValidationError


class ApplicationFormCreateSerializer(ModelSerializer):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    class Meta:
        model = GoElectricRebateApplication
        exclude = ["user", "status", "tax_year"]

    def _get_tax_year(self):
        today = date.today()
        month = today.month
        year = today.year
        if month < 7:
            return year - 2
        return year - 1


class ApplicationFormCreateSerializerDefault(ApplicationFormCreateSerializer):
    def validate(self, data):
        if data.get("doc1") is None or data.get("doc2") is None:
            raise ValidationError("Missing required document.")
        validate_file_size(data["doc1"])
        validate_file_size(data["doc2"])
        return data

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        spouse_email = request.data.get("spouse_email")

        obj = GoElectricRebateApplication.objects.create(
            sin=validated_data["sin"],
            status=self._get_status(validated_data),
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
            spouse_email=spouse_email,
            user=user,
            consent_personal=validated_data["consent_personal"],
            consent_tax=validated_data["consent_tax"],
        )
        return obj

    def _get_status(self, validated_data):
        application_type = validated_data["application_type"]
        # TODO use enum type here like status.
        if application_type == "household":
            return GoElectricRebateApplication.Status.HOUSEHOLD_INITIATED
        return GoElectricRebateApplication.Status.SUBMITTED


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
        spouse_email = request.data.get("spouse_email")

        obj = GoElectricRebateApplication.objects.create(
            sin=validated_data["sin"],
            status=self._get_status(validated_data),
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
            spouse_email=spouse_email,
            user=user,
            consent_personal=validated_data["consent_personal"],
            consent_tax=validated_data["consent_tax"],
        )
        return obj

    def _get_status(self, validated_data):
        application_type = validated_data["application_type"]
        # TODO use enum type here like status.
        if application_type == "household":
            return GoElectricRebateApplication.Status.HOUSEHOLD_INITIATED
        return GoElectricRebateApplication.Status.VERIFIED


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


class ApplicationFormSpouseSerializer(ModelSerializer):
    class Meta:
        model = GoElectricRebateApplication
        fields = [
            "address",
            "city",
            "postal_code",
        ]
