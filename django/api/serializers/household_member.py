from rest_framework.serializers import ModelSerializer, SerializerMethodField
from api.models.household_member import HouseholdMember
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from rest_framework.parsers import FormParser, MultiPartParser


class HouseholdMemberApplicationCreateSerializer(ModelSerializer):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    class Meta:
        model = HouseholdMember
        exclude = ["user"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, validated_data):
        request = self.context.get("request")
        user = self.context["request"].user

        obj = HouseholdMember.objects.create(
            application=validated_data["application"],
            sin=validated_data["sin"],
            email=validated_data["email"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            middle_names=validated_data["middle_names"],
            date_of_birth=validated_data["date_of_birth"],
            doc1=validated_data["doc1"],
            doc2=validated_data["doc2"],
            verified=False,
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

    def get_sin(self, obj):
        return "******" + str(obj.sin)[-3:]

    class Meta:
        model = HouseholdMember
        fields = (
            "application_id",
            "address",
            "city",
            "postal_code",
            "tax_year",
            "first_name",
            "middle_names",
            "last_name",
            "sin",
            "email",
            "date_of_birth",
            "doc1",
            "doc2",
            "consent_personal",
            "consent_tax",
            "created",
        )


class HouseholdMemberApplicationAddressSerializer(ModelSerializer):
    class Meta:
        model = GoElectricRebateApplication
        fields = ("address", "city", "postal_code", "id", "tax_year")
