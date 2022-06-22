import requests
import json
from django.conf import settings
from api.models.go_electric_rebate import GoElectricRebate


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
def notify(drivers_licence, last_name, expiry_date, rebate_amount, rebate_id):
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
    payload = json.dumps(
        {
            "__metadata": {"type": "SP.Data.ITVREligibilityListItem"},
            "Title": drivers_licence,
            "LastName": last_name,
            "ExpiryDT": expiry_date,
            "MaxRebateAmt": rebate_amount,
            "Status": "Not-Redeemed",
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
    print(ncda_rs.text)

    ncda_rs.raise_for_status()

    data = ncda_rs.json()
    ncda_id = data["d"]["ID"]

    GoElectricRebate.objects.filter(pk=rebate_id).update(ncda_id=ncda_id)


# https://support.shortpoint.com/support/solutions/articles/1000307202-shortpoint-rest-api-selecting-filtering-sorting-results-in-a-sharepoint-list

# https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/web/lists/getbytitle('ITVREligibility')/items?$select=Title,Status

# https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/web/lists/getbytitle('ITVREligibility')/items?$select=Title,Created,Status&$orderby=Created desc

# https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/web/lists/getbytitle('ITVREligibility')/items?$select=Title,Modified,Status&$orderby=Modified desc&$filter=Modified ge datetime'2022-06-20T00:00:00Z'

# https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/web/lists/getbytitle('ITVREligibility')/items?$select=Title,Modified,Status&$orderby=Modified desc&$filter=Status eq 'Redeemed'

# https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/web/lists/getbytitle('ITVREligibility')/items?$select=Title,Modified,Status&$orderby=Modified desc&$filter=(Status eq 'Redeemed')and(Modified ge datetime'2022-06-20T00:00:00Z')

# https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/web/lists/getbytitle('ITVREligibility')/items?$select=Id,Title,Modified,Status&$orderby=Modified desc&$filter=(Status eq 'Redeemed')and(Modified ge datetime'2022-06-09T00:00:00Z')


# Example API response with one Sharepoint list item.
# {
#     "d": {
#         "results": [
#             {
#                 "__metadata": {
#                     "id": "e2356fcb-8649-4cc4-81b5-d16fa330244f",
#                     "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)",
#                     "etag": '"3"',
#                     "type": "SP.Data.ITVREligibilityListItem",
#                 },
#                 "FirstUniqueAncestorSecurableObject": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/FirstUniqueAncestorSecurableObject"
#                     }
#                 },
#                 "RoleAssignments": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/RoleAssignments"
#                     }
#                 },
#                 "AttachmentFiles": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/AttachmentFiles"
#                     }
#                 },
#                 "ContentType": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/ContentType"
#                     }
#                 },
#                 "GetDlpPolicyTip": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/GetDlpPolicyTip"
#                     }
#                 },
#                 "FieldValuesAsHtml": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/FieldValuesAsHtml"
#                     }
#                 },
#                 "FieldValuesAsText": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/FieldValuesAsText"
#                     }
#                 },
#                 "FieldValuesForEdit": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/FieldValuesForEdit"
#                     }
#                 },
#                 "File": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/File"
#                     }
#                 },
#                 "Folder": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/Folder"
#                     }
#                 },
#                 "LikedByInformation": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/LikedByInformation"
#                     }
#                 },
#                 "ParentList": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/ParentList"
#                     }
#                 },
#                 "Properties": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/Properties"
#                     }
#                 },
#                 "Versions": {
#                     "__deferred": {
#                         "uri": "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/Web/Lists(guid'7aea54d3-9935-40a4-88cd-3ddd74c7d270')/Items(5)/Versions"
#                     }
#                 },
#                 "FileSystemObjectType": 0,
#                 "Id": 5,
#                 "ServerRedirectedEmbedUri": null,
#                 "ServerRedirectedEmbedUrl": "",
#                 "ID": 5,
#                 "ContentTypeId": "0x01008074AAC5CAD1A241B1109194FE6D8D5D00747BB541D61F1F4CA7028C9C97E823CB",
#                 "Title": "44444444",
#                 "Modified": "2022-06-09T06:01:10Z",
#                 "Created": "2022-06-07T16:22:31Z",
#                 "AuthorId": 1073741822,
#                 "EditorId": 1073741822,
#                 "OData__UIVersionString": "3.0",
#                 "Attachments": false,
#                 "GUID": "cf205d6e-b0f1-481e-8988-4aa1119a4033",
#                 "ComplianceAssetId": null,
#                 "LastName": "Test4",
#                 "ExpiryDT": "2023-08-01T07:00:00Z",
#                 "MaxRebateAmt": 1500,
#                 "Status": "Redeemed",
#                 "ClaimType": null,
#                 "OData__vti_ItemDeclaredRecord": null,
#             }
#         ]
#     }
# }
