from django import forms
from api.models.go_electric_rebate_application import ExpiredGoElectricRebateApplication
from api.constants import ONE_THOUSAND_REBATE, TWO_THOUSAND_REBATE, FOUR_THOUSAND_REBATE


class ExtendExpiryForm(forms.ModelForm):
    rebate_amount = forms.ChoiceField(
        choices=[
            (ONE_THOUSAND_REBATE.ZEV_MAX.value, ONE_THOUSAND_REBATE.ZEV_MAX.value),
            (TWO_THOUSAND_REBATE.ZEV_MAX.value, TWO_THOUSAND_REBATE.ZEV_MAX.value),
            (FOUR_THOUSAND_REBATE.ZEV_MAX.value, FOUR_THOUSAND_REBATE.ZEV_MAX.value),
        ]
    )

    class Meta:
        model = ExpiredGoElectricRebateApplication
        fields = "__all__"
