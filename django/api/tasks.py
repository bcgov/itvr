import requests
import json

from django.conf import settings
from email.header import Header
from email.utils import formataddr
from requests.auth import HTTPBasicAuth


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
    recipient_email: str,
    application_id: str,
    message: str,
    cc_list: list,
    optional_subject="",
) -> None:
    sender_email = settings.EMAIL["SENDER_EMAIL"]
    sender_name = settings.EMAIL["SENDER_NAME"]
    url = settings.EMAIL["CHES_EMAIL_URL"]

    subject = (
        "CleanBC Go Electric - Application #{}".format(application_id)
        + optional_subject
    )
    bodyType = "html"

    auth_token = get_email_service_token()
    sender_info = formataddr((str(Header(sender_name, "utf-8")), sender_email))

    data = {
        # "bcc": [recipient_email],
        "bodyType": bodyType,
        "body": message,
        "cc": cc_list,
        "delayTS": 0,
        "encoding": "utf-8",
        "from": sender_info,
        "priority": "normal",
        "subject": subject,
        # "to": ["Undisclosed recipients<donotreply@gov.bc.ca>"],
        "to": [recipient_email],
    }

    headers = {
        "Authorization": "Bearer " + auth_token,
        "Content-Type": "application/json",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.raise_for_status()


def send_individual_confirm(recipient_email, application_id):
    message = """\
        <html>
        <body>

        <p>
        This email was generated by the CleanBC Go Electric
        Passenger Vehicle Rebate program application.
        </p>

        <p>
        We have received your application for a rebate under the CleanBC Go
        Electric Passenger Vehicle Rebate program.
        </p>

        <p>Please keep this e-mail for your records.</p>

        <p>Questions?</p>

        <p>Please feel free to contact us at ZEVPrograms@gov.bc.ca</p>
        </body>
        </html>
        """
    send_email(recipient_email, application_id, message, cc_list=[])


def send_spouse_initial_message(recipient_email, application_id, initiator_email):
    origin = settings.CORS_ORIGIN_WHITELIST[0]
    message = """\
        <html>
        <body>

        <p>
        This email was generated by the CleanBC Go Electric
        Passenger Vehicle Rebate program application.
        </p>

        <p>Dear Applicant,</p>

        <p>
        You are receiving this e-mail as you have been identified as a
        spouse under a household rebate application for the CleanBC Go
        Electric Passenger Vehicle Rebate program.
        </p>

        <p>
        To finish the rebate application please click on the
        following link:
        </p>

        <p>{origin}/household?q={application_id}</p>

        <p>
        If you are not the intended person to receive this email, please
        contact the CleanBC Go Electric Passenger Vehicle Rebate program at
        ZEVPrograms@gov.bc.ca
        </p>

        <p>Additional Questions?</p>

        <p>Please feel free to contact us at ZEVPrograms@gov.bc.ca</p>
        </body>
        </html>
        """.format(
        origin=origin, application_id=application_id
    )
    send_email(recipient_email, application_id, message, [initiator_email])


def send_household_confirm(recipient_email, application_id):
    message = """\
        <html>
        <body>

        <p>
        This email was generated by the CleanBC Go Electric
        Passenger Vehicle Rebate program application.
        </p>

        <p>Thank you.</p>

        <p>
        We have now received all documentation for your application for a
        household rebate under the CleanBC Go Electric Passenger Vehicle
        Rebate program.
        </p>

        <p>Please keep this e-mail for your records.</p>

        <p>Questions?</p>

        <p>Please feel free to contact us at ZEVPrograms@gov.bc.ca</p>

        </body>
        </html>
        """
    send_email(recipient_email, application_id, message, cc_list=[])


def send_reject(recipient_email, application_id):
    message = """\
        <html>
        <body>

        <p>This email was generated by the CleanBC Go Electric Passenger
        Vehicle Rebate program application.</p>

        <p> Dear Applicant,</p>

        <p>You are receiving this e-mail as a response to your application for
        a rebate under the CleanBC Go Electric Passenger Vehicle Rebate
        program.</p>

        <p>We would like to notify you, that your application has not been
        approved.</p>

        <p>Some examples of why this may have happened include:</p>

        <ul>
            <li>
                No record of your 2020 Notice of Assessment on file with the Canada Revenue Agency (CRA).
            </li>
        
            <li>
                The identity records that you have supplied do not match CRA records.
            </li>

            <li>
                Your income does not qualify/exceeds the maximum eligible amount under the program.
            </li>
            <li>
                Household application addresses are not the same
                for applicant and spouse.
            </li>
        </ul>

        <p>Questions?</p>

        <p>Please feel free to contact us at ZEVPrograms@gov.bc.ca</p>
        </body>
        </html>
         """
    send_email(
        recipient_email,
        application_id,
        message,
        cc_list=[],
        optional_subject=" – Not Approved",
    )


def send_approve(recipient_email, application_id):
    message = """\
        <html>
        <body>

        <p>This email was generated by the CleanBC Go Electric Passenger
        Vehicle Rebate program application.</p>

        <p> Dear Applicant,</p>

        <p>You are receiving this e-mail as a response to your application for
        a rebate under the CleanBC Go Electric Passenger Vehicle Rebate
        program.</p>

        <p>We would like to notify you, that your application has been approved
        and you are entitled to a maximum rebate amount of $X,XXX.</p>

        <p>Your rebate will expire one year from today’s date.</p>
        
        <p>Next steps:</p>
        <ol>
          <li>
          Please allow X business days for your information to be populated into
          the rebate database at B.C. automotive dealerships.</li>
          <li>
            Bring your drivers license with you to an automotive dealer in B.C.
          </li>
          <li>
            Use your rebate at the time of vehicle purchase to realize cost savings
            on your new zero-emission vehicle!
          </li>
        </ol>
        <p>Please note: This e-mail confirms that you have been approved for a
        rebate under the CleanBC Go Electric Light-Duty Vehicle program only.
        Accessing the rebate is conditional on Program funds being available
        at the time of vehicle purchase.</p>

        <p>Questions?</p>

        <p>Please feel free to contact us at ZEVPrograms@gov.bc.ca</p>
        </body>
        </html>
         """
    send_email(
        recipient_email,
        application_id,
        message,
        cc_list=[],
        optional_subject=" – Approved",
    )
