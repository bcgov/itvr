import requests
import json
from django.utils import timezone

from django.conf import settings
from email.header import Header
from email.utils import formataddr
from requests.auth import HTTPBasicAuth
from api.services.ncda import get_rebates_redeemed_since
from api.models.go_electric_rebate import GoElectricRebate
from api.models.go_electric_rebate_application import (
    GoElectricRebateApplication,
)
from datetime import timedelta
from django.db.models.signals import post_save


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

        <p>Thank you.</p>

        <p>
        We have received your application for a rebate under the CleanBC Go
        Electric Passenger Vehicle Rebate program. You can expect to get an email reply with the result of your application within 3 weeks.
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
        You are receiving this e-mail as you have been identified as a
        spouse under a household rebate application for the CleanBC Go
        Electric Passenger Vehicle Rebate program.
        </p>

        <p>
        To finish the rebate application please click on the
        following link:
        </p>

        <p>{origin}/household?q={application_id}</p>

        <p><i>
        If you are not the intended person to receive this email, please
        contact the CleanBC Go Electric Passenger Vehicle Rebate program at
        ZEVPrograms@gov.bc.ca
        </i></p>

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
        Rebate program. You can expect to get an email reply with the result of your application within 3 weeks.
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

        <p>Dear Applicant,</p>

        <p>Your application has not been approved.</p>

        <p>Some examples of why this may have happened include:</p>

        <ul>
            <li>
                Driver???s license/secondary piece of ID quality not sufficient, identification documents don???t match.
            </li>
            <li>
                Household application addresses are not the same
                for applicant and spouse.
            </li>
        </ul>

        <p>You are encouraged to correct these issues and submit another application.</p>

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
        optional_subject=" ??? Not Approved",
    )


def send_approve(recipient_email, application_id, rebate_amount):
    message = """\
        <html>
        <body>

        <p>This email was generated by the CleanBC Go Electric Passenger
        Vehicle Rebate program application.</p>

        <p>Dear Applicant,</p>

        <p>
        Your application has been approved for a rebate amount of up to ${rebate_amount}.
        The full amount applies to purchases of battery electric and long-range plug-in hybrids.
        For plug-in hybrids with ranges less than 85 km the rebate amount is half.
        </p>

        <p>Your rebate will expire one year from today???s date.</p>
        
        <p>Next steps:</p>
        <ol>
          <li>
            Your approval is now linked to your driver???s licence. Bring your driver's licence with you to a new car dealer in B.C.
          </li>
          <li>
            Claim your rebate at the time of vehicle purchase to save money on your new zero-emission vehicle!
          </li>
        </ol>
        <p><i>Please note: This e-mail confirms that you have been approved for a
        rebate under the CleanBC Go Electric Light-Duty Vehicle program only.
        Accessing the rebate is conditional on Program funds being available
        at the time of vehicle purchase.</i></p>

        <p>Questions?</p>

        <p>Please feel free to contact us at ZEVPrograms@gov.bc.ca</p>
        </body>
        </html>
         """.format(
        rebate_amount=rebate_amount
    )
    send_email(
        recipient_email,
        application_id,
        message,
        cc_list=[],
        optional_subject=" ??? Approved",
    )


def send_not_approve(recipient_email, application_id, tax_year):
    message = """\
        <html>
        <body>

        <p>This email was generated by the CleanBC Go Electric Passenger
        Vehicle Rebate program application.</p>

        <p>Dear Applicant,</p>

        <p>Your application has not been approved.</p>

        <p>Some examples of why this may have happened include:</p>

        <ul>
            <li>
                No record of your {tax_year} Notice of Assessment on file with the Canada Revenue Agency (CRA).
            </li>
            <li>
                The identity records that you have supplied do not match CRA records.
            </li>
            <li>
                Your income does not qualify/exceeds the maximum eligible amount under the program.
            </li>
        </ul>

        <p>Questions?</p>

        <p>Please feel free to contact us at ZEVPrograms@gov.bc.ca</p>
        </body>
        </html>
         """.format(
        tax_year=tax_year
    )
    send_email(
        recipient_email,
        application_id,
        message,
        cc_list=[],
        optional_subject=" ??? Not Approved",
    )


def send_cancel(recipient_email, application_id):
    message = """\
        <html>
        <body>

        <p>This email was generated by the CleanBC Go Electric Passenger
        Vehicle Rebate program application.</p>

        <p>Your application has been cancelled.</p>

        <p>Some examples of why this may have happened include:</p>

        <ul>
            <li>
                The person you identified as your spouse cancelled the application.
            </li>
            <li>
                The person you identified as your spouse didn???t complete the application within 28 days.
            </li>
        </ul>

        <p>You are encouraged to apply again as an individual if your spouse is unable to complete the household application.</p>

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
        optional_subject=" ??? Cancelled",
    )


# check for newly redeemed rebates
def check_rebates_redeemed_since(iso_ts=None):
    ts = iso_ts if iso_ts else timezone.now().strftime("%Y-%m-%dT00:00:00Z")
    print("check_rebate_status " + ts)
    ncda_ids = get_rebates_redeemed_since(ts)
    print(ncda_ids)

    redeemed_rebates = GoElectricRebate.objects.filter(ncda_id__in=ncda_ids)

    # mark redeemed
    redeemed_rebates.update(redeemed=True, modified=timezone.now())
    # update application status
    GoElectricRebateApplication.objects.filter(
        pk__in=list(redeemed_rebates.values_list("application_id", flat=True))
    ).update(
        status=GoElectricRebateApplication.Status.REDEEMED,
        modified=timezone.now(),
    )


# cancels household_initiated applications with a created_time <= (current_time - 28 days)
def cancel_untouched_household_applications():

    applications_qs = GoElectricRebateApplication.objects.filter(
        status=GoElectricRebateApplication.Status.HOUSEHOLD_INITIATED
    ).filter(created__lte=timezone.now() - timedelta(days=28))

    applications = list(applications_qs)

    applications_qs.update(
        status=GoElectricRebateApplication.Status.CANCELLED,
        modified=timezone.now(),
    )

    for application in applications:
        application.status = GoElectricRebateApplication.Status.CANCELLED
        post_save.send(
            sender=GoElectricRebateApplication,
            instance=application,
            created=False,
            update_fields={"status"},
        )
