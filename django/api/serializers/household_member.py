from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
from api.models.household_member import HouseholdMember
from rest_framework.parsers import FormParser, MultiPartParser


class HouseholdMemberApplicationCreateSerializer(ModelSerializer):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def validate(self, data):
        user_id = self.context["request"].user.id
        application_user_id = data["application"].user.id
        if user_id == application_user_id:
            raise ValidationError("spouse cannot be the same as the main applicant")
        return data

    class Meta:
        model = HouseholdMember
        exclude = ["user", "bcsc_address", "bcsc_city", "bcsc_postal_code"]


class HouseholdMemberApplicationCreateSerializerDefault(
    HouseholdMemberApplicationCreateSerializer
):
    def create(self, validated_data):
        user = self.context["request"].user

        obj = HouseholdMember.objects.create(
            application=validated_data["application"],
            sin=validated_data["sin"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            middle_names=validated_data["middle_names"],
            date_of_birth=validated_data["date_of_birth"],
            doc1=validated_data["doc1"],
            doc2=validated_data["doc2"],
            user=user,
            consent_personal=validated_data["consent_personal"],
            consent_tax=validated_data["consent_tax"],
        )
        return obj


class HouseholdMemberApplicationCreateSerializerBCSC(
    HouseholdMemberApplicationCreateSerializer
):
    class Meta(HouseholdMemberApplicationCreateSerializer.Meta):
        exclude = [
            "last_name",
            "first_name",
            "middle_names",
            "date_of_birth",
            "doc1",
            "doc2",
        ] + HouseholdMemberApplicationCreateSerializer.Meta.exclude

    def create(self, validated_data):
        user = self.context["request"].user

        obj = HouseholdMember.objects.create(
            application=validated_data["application"],
            sin=validated_data["sin"],
            last_name=user.last_name,
            first_name=user.first_name,
            date_of_birth=user.date_of_birth,
            bcsc_address=user.street_address,
            bcsc_city=user.locality,
            bcsc_postal_code=user.postal_code,
            user=user,
            consent_personal=validated_data["consent_personal"],
            consent_tax=validated_data["consent_tax"],
        )
        return obj


class HouseholdMemberApplicationGetSerializer(ModelSerializer):
    application_id = SerializerMethodField()
    sin = SerializerMethodField()
    address = SerializerMethodField()
    city = SerializerMethodField()
    postal_code = SerializerMethodField()
    tax_year = SerializerMethodField()
    application_type = SerializerMethodField()
    status = SerializerMethodField()

    def get_address(self, obj):
        return obj.application.address

    def get_city(self, obj):
        return obj.application.city

    def get_postal_code(self, obj):
        return obj.application.postal_code

    def get_tax_year(self, obj):
        return obj.application.tax_year

    def get_application_id(self, obj):
        return obj.application.id

    def get_application_type(self, obj):
        return obj.application.application_type

    def get_status(self, obj):
        return obj.application.status

    def get_sin(self, obj):
        return "******" + str(obj.sin)[-3:]

    class Meta:
        model = HouseholdMember
        fields = (
            "application_id",
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
        )
