# django_q hooks


from api.models.go_electric_rebate_application import GoElectricRebateApplication


def set_email_status(task):
    func = task.func
    application_id = task.args[1]
    email_successful = task.success
    if func == "api.tasks.send_individual_confirm":
        GoElectricRebateApplication.objects.filter(pk=application_id).update(
            confirmation_email_success=email_successful
        )