import requests
import json
from unidecode import unidecode
from django.conf import settings


def read(file):
    results = {}
    current_application_id = None
    current_application = None
    for line in file.split("\n"):
        # Grab the sub-code, defining type of record.
        subCode = line[17:21]

        # CRA-RESPONSE-0022
        if subCode == "0022":
            current_application_id = line[41:57]
            if current_application_id not in results:
                results[current_application_id] = []
            current_application = results[current_application_id]

            # REQUEST-STATUS-CODE
            status_code = line[25:27]
            # 55 UNSUCCESSFUL-ACCT-NOT-AVAIL
            # 59 UNSUCCESSFUL-REQUEST NO DATA
            if status_code in ["59", "55"]:
                sin = line[4:13]
                year = line[13:17]
                current_application.append({"sin": sin, "year": year, "income": None})

        # From Susan:
        # The business folks did flip flop on the net income
        # (record 0236) line 23600 vs total income (0150)
        # but total income (record 0150) or line 15000 was the final decision.
        if subCode == "0150":
            sin = line[4:13]
            year = line[13:17]
            income = line[21:30].lstrip("0")
            if income == "":
                income = "0"
            current_application.append({"sin": sin, "year": year, "income": income})
    return results


def write(
    data, today="20220516", program_code="BCVR", cra_env="A", cra_sequence="00001"
):
    file = ""

    # Number of records to write.
    lines = str(len(data) + 2)  # Includes header and footer.
    records = "0" * (8 - len(lines)) + lines

    # Write the header
    file += "7100"  # Request transaction code
    file += " " * 24  # Blank space

    file += today  #
    file += " "  # Blank space

    file += program_code + cra_env + cra_sequence

    file += " " * 99  # Blank space

    file += "0\n"  # Blank space

    # Write the body
    for row in data:
        sin = row["sin"]
        family_name = unidecode(row["family_name"].ljust(30)[:30])
        given_name = unidecode(row["given_name"].ljust(30)[:30])
        tax_years = " ".join([str(year) for year in row["years"]]).ljust(20)
        birth_date = row["birth_date"]
        identifier = row["application_id"].ljust(30)
        row = f"7101{sin}    0020{family_name}{given_name}{birth_date}{tax_years}{program_code}{identifier}   0\n"
        file += row

    # Write the trailer
    file += "7102"  # Request transaction code
    file += " " * 24  # Blank space

    file += today  # Request date
    file += " "  # Blank space

    file += program_code + cra_env + cra_sequence

    file += " " * 6  # Blank space

    file += records  # Number of records in file

    file += " " * 85  # Blank space

    file += "0"  # terminating character

    return file


def decrypt_file(file):
    url = settings.CRYPTO_SERVICE_URL + "/decrypt"
    data = file.read()
    response = requests.get(
        url,
        data=data,
        auth=(settings.EPF_FILENAME, settings.EPF_PASSWORD),
        verify=True,
    )
    response.raise_for_status()
    return response.text


def encrypt(to_encrypt):
    url = settings.CRYPTO_SERVICE_URL + "/encrypt"
    payload = {"certificate": settings.CRA_CERTIFICATE, "toEncrypt": to_encrypt}
    if settings.CRA_CERTIFICATE_CRL_DN:
        payload["crlDN"] = settings.CRA_CERTIFICATE_CRL_DN
    payload_json = json.dumps(payload)
    headers = {"content-type": "application/json"}
    response = requests.get(
        url,
        data=payload_json,
        headers=headers,
        auth=(settings.EPF_FILENAME, settings.EPF_PASSWORD),
        verify=True,
    )
    response.raise_for_status()
    return response.content
