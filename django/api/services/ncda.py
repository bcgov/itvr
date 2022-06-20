import requests
import json
from django.conf import settings


def get_ncda_service_token() -> str:
    client_id = settings.NCDA_CLIENT_ID
    client_secret = settings.NCDA_CLIENT_SECRET
    resource = settings.NCDA_RESOURCE
    url = settings.NCDA_AUTH_URL
    payload = {
        "grant_type": "client_credentials",
        "client_credentials": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "resource": resource,
    }

    headers = {"content-type": "application/x-www-form-urlencoded"}

    token_rs = requests.post(
        url,
        data=payload,
        headers=headers,
        verify=True,
    )
    token_rs.raise_for_status()
    return token_rs.json()["access_token"]


# Tell NCDA about a newly issued rebate.
def notify(drivers_licence, last_name, expiry_date, rebate_amount):
    api_endpoint = settings.NCDA_SHAREPOINT_URL
    access_token = get_ncda_service_token()

    # {
    #     "__metadata": {"type": "SP.Data.ITVREligibilityListItem"},
    #     "Title": "77777777",
    #     "LastName": "Test7",
    #     "ExpiryDT": "6/22/2023",
    #     "MaxRebateAmt": "1500",
    #     "Status": "Not-Redeemed",
    # }
    payload = {
        "__metadata": {"type": "SP.Data.ITVREligibilityListItem"},
        "Title": drivers_licence,
        "LastName": last_name,
        "ExpiryDT": expiry_date,
        "MaxRebateAmt": rebate_amount,
        "Status": "Not-Redeemed",
    }

    print(payload)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }

    url = api_endpoint + "/lists/getbytitle('ITVREligibility')/items"
    print(url)
    ncda_rs = requests.post(
        url,
        data=payload,
        headers=headers,
        verify=True,
    )

    print(ncda_rs)

    ncda_rs.raise_for_status()
