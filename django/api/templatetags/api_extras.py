from django import template
from api.models.go_electric_rebate_application import GoElectricRebateApplication

register = template.Library()


@register.simple_tag
def get_verified_rebates_count():
    return GoElectricRebateApplication.objects.filter(
        status=GoElectricRebateApplication.Status.VERIFIED
    ).count()
