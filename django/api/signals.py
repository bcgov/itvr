import logging
import requests
import json

from django.db.models.signals import post_save
from .models.go_electric_rebate_application import GoElectricRebateApplication
from django.dispatch import receiver
from django.conf import settings
from email.header import Header
from email.utils import formataddr
from requests.auth import HTTPBasicAuth

from api.models.household_member import HouseholdMember

LOGGER = logging.getLogger(__name__)


def get_email_service_token() -> {}:
    client_id = settings.EMAIL["EMAIL_SERVICE_CLIENT_ID"]
    client_secret = settings.EMAIL["EMAIL_SERVICE_CLIENT_SECRET"]
    url = settings.EMAIL["CHES_AUTH_URL"]
    payload = {"grant_type": "client_credentials"}
    header = {"content-type": "application/x-www-form-urlencoded"}

    try:
        token_rs = requests.post(
            url,
            data=payload,
            auth=HTTPBasicAuth(client_id, client_secret),
            headers=header,
            verify=True,
        )
        if not token_rs.status_code == 200:
            LOGGER.error("Error: Unexpected response", token_rs.text.encode("utf8"))
            return
        json_obj = token_rs.json()
        return json_obj
    except requests.exceptions.RequestException as e:
        LOGGER.error("Error: {}".format(e))
        return


def send_email(
    recipient_email: str, application_id: str, message: str, cc_list: list
) -> {}:
    sender_email = settings.EMAIL["SENDER_EMAIL"]
    sender_name = settings.EMAIL["SENDER_NAME"]
    url = settings.EMAIL["CHES_EMAIL_URL"]

    subject = "CleanBC Go Electric - Application #{}".format(application_id)
    bodyType = "html"

    token = get_email_service_token()
    if not token or "access_token" not in token:
        LOGGER.error("No email service token provided", token)
        return
    auth_token = token["access_token"]

    sender_info = formataddr((str(Header(sender_name, "utf-8")), sender_email))

    data = {
        "bcc": [recipient_email],
        "bodyType": bodyType,
        "body": message,
        "cc": cc_list,
        "delayTS": 0,
        "encoding": "utf-8",
        "from": sender_info,
        "priority": "normal",
        "subject": subject,
        "to": ["Undisclosed recipients<donotreply@gov.bc.ca>"],
    }

    headers = {
        "Authorization": "Bearer " + auth_token,
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if not response.status_code == 201:
            LOGGER.error("Error: Email failed! %s", response.text.encode("utf8"))
            return

        email_res = response.json()
        if email_res:
            LOGGER.debug("Email sent successfully!", email_res["messages"][0]["msgId"])
            return
    except requests.exceptions.RequestException as e:
        LOGGER.error("Error: {}".format(e))
        return


def send_individual_confirm(recipient, id):
    message = """
        We have received your application for a rebate under the CleanBC Go Electric Passenger Vehicle Rebate program.

        Please keep this e-mail for your records.

        Questions?

        Please feel free to contact us at ZEVPrograms@gov.bc.ca
        """
    send_email(recipient, id, message, cc_list=[])


def send_spouse_initial_message(recipient, id, initiator_email):
    message = """
        Dear Applicant,

        You are receiving this e-mail as you have been identified as a spouse under a household rebate application for the CleanBC Go Electric Light-Duty Vehicle program.

        To finish the rebate application please click on the following link:

        http://localhost:3000/household?q={}

        Questions?

        Please feel free to contact us at ZEVPrograms@gov.bc.ca
        """.format(
        id
    )
    send_email(recipient, id, message, cc_list=[initiator_email])


# TODO have this schedule an email task that's retried in the future incase
# CHES has issues when we setup celery.
@receiver(post_save, sender=GoElectricRebateApplication)
def create_application(sender, instance, created, **kwargs):
    if created and settings.EMAIL["SEND_EMAIL"]:
        send_individual_confirm(recipient=instance.email, id=instance.id)
        if instance.application_type == "household":
            send_spouse_initial_message(
                recipient=instance.spouse_email,
                id=instance.id,
                initiator_email=instance.email,
            )
