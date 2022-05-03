import logging
import requests
import json

from django.conf import settings
from email.header import Header
from email.utils import formataddr
from requests.auth import HTTPBasicAuth

LOGGER = logging.getLogger(__name__)


def get_email_service_token() -> str:
    client_id = settings.EMAIL["EMAIL_SERVICE_CLIENT_ID"]
    client_secret = settings.EMAIL["EMAIL_SERVICE_CLIENT_SECRET"]
    url = settings.EMAIL["CHES_AUTH_URL"]
    payload = {"grant_type": "client_credentials"}
    header = {"content-type": "application/x-www-form-urlencoded"}

    token_rs = requests.post(
        url,
        data=payload,
        auth=HTTPBasicAuth(client_id, client_secret),
        headers=header,
        verify=True,
    )
    token_rs.raise_for_status()
    return token_rs.json()["access_token"]


def send_email(
    recipient_email: str, application_id: str, message: str, cc_list: list
) -> None:
    sender_email = settings.EMAIL["SENDER_EMAIL"]
    sender_name = settings.EMAIL["SENDER_NAME"]
    url = settings.EMAIL["CHES_EMAIL_URL"]

    subject = "CleanBC Go Electric - Application #{}".format(application_id)
    bodyType = "html"

    auth_token = get_email_service_token()
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

    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.raise_for_status()


def send_individual_confirm(recipient_email, application_id):
    message = """
        We have received your application for a rebate under the CleanBC Go Electric Passenger Vehicle Rebate program.

        Please keep this e-mail for your records.

        Questions?

        Please feel free to contact us at ZEVPrograms@gov.bc.ca
        """
    send_email(recipient_email, application_id, message, cc_list=[])


def send_spouse_initial_message(recipient_email, application_id, initiator_email):
    origin = settings.CORS_ORIGIN_WHITELIST[0]
    message = """
        Dear Applicant,

        You are receiving this e-mail as you have been identified as a spouse under a household rebate application for the CleanBC Go Electric Light-Duty Vehicle program.

        To finish the rebate application please click on the following link:

        {origin}/household?q={application_id}

        Questions?

        Please feel free to contact us at ZEVPrograms@gov.bc.ca
        """.format(
        origin=origin, application_id=application_id
    )
    send_email(recipient_email, application_id, message, [initiator_email])


def send_household_confirm(recipient_email, application_id, initiator_email):
    message = """
        Thank you.

        We have now received all documentation for your application for a household rebate under the CleanBC Go Electric Passenger Vehicle Rebate program.

        Please keep this e-mail for your records.

        Questions?

        Please feel free to contact us at ZEVPrograms@gov.bc.ca
        """
    send_email(recipient_email, application_id, message, [initiator_email])
