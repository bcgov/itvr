import requests
import json
from django.conf import settings

# sample response from ncda when posting a rebate to ncda:

# {
#     "d": {
#         "__metadata": {
#             "id": "57bc90e6-6774-416e-8daa-090385ef8f45",
#             "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)",
#             "etag": '"1"',
#             "type": "SP.Data.ITVREligibilityListItem",
#         },
#         "FirstUniqueAncestorSecurableObject": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/FirstUniqueAncestorSecurableObject"
#             }
#         },
#         "RoleAssignments": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/RoleAssignments"
#             }
#         },
#         "AttachmentFiles": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/AttachmentFiles"
#             }
#         },
#         "ContentType": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/ContentType"
#             }
#         },
#         "GetDlpPolicyTip": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/GetDlpPolicyTip"
#             }
#         },
#         "FieldValuesAsHtml": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/FieldValuesAsHtml"
#             }
#         },
#         "FieldValuesAsText": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/FieldValuesAsText"
#             }
#         },
#         "FieldValuesForEdit": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/FieldValuesForEdit"
#             }
#         },
#         "File": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/File"
#             }
#         },
#         "Folder": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/Folder"
#             }
#         },
#         "LikedByInformation": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/LikedByInformation"
#             }
#         },
#         "ParentList": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/ParentList"
#             }
#         },
#         "Properties": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/Properties"
#             }
#         },
#         "Versions": {
#             "__deferred": {
#                 "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(19)/Versions"
#             }
#         },
#         "FileSystemObjectType": 0,
#         "Id": 19,
#         "ServerRedirectedEmbedUri": null,
#         "ServerRedirectedEmbedUrl": "",
#         "ID": 19,
#         "ContentTypeId": "0x01008074AAC5CAD1A241B1109194FE6D8D5D00747BB541D61F1F4CA7028C9C97E823CB",
#         "Title": "23456781",
#         "Modified": "2022-06-16T22:51:39Z",
#         "Created": "2022-06-16T22:51:39Z",
#         "AuthorId": 1073741822,
#         "EditorId": 1073741822,
#         "OData__UIVersionString": "1.0",
#         "Attachments": false,
#         "GUID": "9e4bceff-29c5-41d0-889a-c320f32b64da",
#         "ComplianceAssetId": null,
#         "LastName": "Aro",
#         "ExpiryDT": "2023-06-16T07:00:00Z",
#         "MaxRebateAmt": 1400,
#         "Status": "Not-Redeemed",
#         "ClaimType": null,
#         "OData__vti_ItemDeclaredRecord": null,
#     }
# }

# 500 Server Error: Internal Server Error for url:
# is sent for duplicate driver's license no etc. Might come up in dev
# Our unique index on driver's license in the rebate table
# should prevent this in prod.

# sample respnse from ncda when getting a rebate from them:

# {
#     "d": {
#         "results": [
#             {
#                 "__metadata": {
#                     "id": "a27d1060-03b2-4f1a-8006-0205c1ce6c43",
#                     "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)",
#                     "etag": '"3"',
#                     "type": "SP.Data.ITVREligibilityListItem",
#                 },
#                 "Id": 5,
#                 "ID": 5,
#                 "Title": "44444444",
#                 "Modified": "2022-06-09T06:01:10Z",
#                 "Status": "Redeemed",
#             }
#         ]
#     }
# }


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
def notify(drivers_licence, last_name, expiry_date, rebate_amount, application_id):
    api_endpoint = settings.NCDA_SHAREPOINT_URL
    access_token = get_ncda_service_token()

    payload = json.dumps(
        {
            "__metadata": {"type": "SP.Data.ITVREligibilityListItem"},
            "Title": drivers_licence,
            "LastName": last_name,
            "ExpiryDT": expiry_date,
            "MaxRebateAmt": rebate_amount,
            "Status": "Not-Redeemed",
            "ITVRApplicationId": application_id,
        }
    )

    headers = {
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose",
    }

    url = api_endpoint + "/lists/getbytitle('ITVREligibility')/items"

    ncda_rs = requests.post(
        url,
        data=payload,
        headers=headers,
        verify=True,
    )

    print(ncda_rs.text)

    ncda_rs.raise_for_status()

    data = ncda_rs.json()
    return data


# iso_ts ex 2023-08-01T07:00:00Z
def get_rebates_redeemed_since(iso_ts, ncda_ids, next_url):
    api_endpoint = settings.NCDA_SHAREPOINT_URL
    access_token = get_ncda_service_token()

    headers = {
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose",
    }

    if next_url:
        ncda_rs = requests.get(next_url, headers=headers, verify=True)
    else:
        url = api_endpoint + "/lists/getbytitle('ITVREligibility')/items"

        payload = {
            "$select": "Id,Title,Modified,Status",
            "$filter": "(Modified ge datetime'%s')and(Status eq 'Redeemed')" % iso_ts,
            "$top": 1000,
        }
        ncda_rs = requests.get(url, headers=headers, params=payload, verify=True)

    ncda_rs.raise_for_status()

    data = ncda_rs.json()
    items = data["d"]["results"]
    ncda_ids.extend(list(map(lambda item: item["ID"], items)))
    next_url = (data["d"]).get("__next")
    if next_url:
        get_rebates_redeemed_since(iso_ts, ncda_ids, next_url)


def delete_rebate(ncda_id):
    api_endpoint = settings.NCDA_SHAREPOINT_URL
    access_token = get_ncda_service_token()

    headers = {
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose",
        "If-Match": "*",
    }

    url = api_endpoint + "/lists/getbytitle('ITVREligibility')/items(%s)" % ncda_id
    ncda_rs = requests.delete(url, headers=headers, verify=True)
    ncda_rs.raise_for_status()


def get_rebates(filter, fields):
    api_endpoint = settings.NCDA_SHAREPOINT_URL
    access_token = get_ncda_service_token()

    headers = {
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose",
    }

    url = api_endpoint + "/lists/getbytitle('ITVREligibility')/items"

    payload = {
        "$filter": filter,
    }
    if fields:
        payload["$select"] = ",".join(fields)

    ncda_rs = requests.get(url, headers=headers, params=payload, verify=True)
    ncda_rs.raise_for_status()
    data = ncda_rs.json()
    items = data["d"]["results"]

    return items


def get_rebate_by_id(ncda_id, fields=[]):
    filter = "(Id eq %s)" % ncda_id
    rebates = get_rebates(filter, fields)
    if len(rebates) >= 1:
        return rebates[0]
    return None


def get_rebate_by_drivers_licence(drivers_licence, fields=[]):
    filter = "(Title eq '%s')" % drivers_licence
    rebates = get_rebates(filter, fields)
    if len(rebates) >= 1:
        return rebates[0]
    return None


def update_rebate(ncda_id, updated_fields):
    api_endpoint = settings.NCDA_SHAREPOINT_URL
    access_token = get_ncda_service_token()

    headers = {
        "Authorization": "Bearer " + access_token,
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose",
        "If-Match": "*",
    }

    url = api_endpoint + "/lists/getbytitle('ITVREligibility')/items(%s)" % ncda_id

    payload = json.dumps(
        {"__metadata": {"type": "SP.Data.ITVREligibilityListItem"}} | updated_fields
    )

    ncda_rs = requests.patch(
        url,
        data=payload,
        headers=headers,
        verify=True,
    )

    ncda_rs.raise_for_status()
