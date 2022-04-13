from rest_framework.serializers import ModelSerializer
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from rest_framework.parsers import FormParser, MultiPartParser


class ApplicationFormCreateSerializer(ModelSerializer):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    class Meta:
        model = GoElectricRebateApplication
        exclude = ["user"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, validated_data):
        user = self.context["request"].user

        obj = GoElectricRebateApplication.objects.create(
            sin=validated_data["sin"],
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
            tax_year=2021,
            verified=False,
            application_type=validated_data["application_type"],
            spouse_email=validated_data["spouse_email"],
            user=user,
        )
        return obj


class ApplicationFormSerializer(ModelSerializer):
    class Meta:
        model = GoElectricRebateApplication
        fields = "__all__"
