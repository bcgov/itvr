##
# Read a text file that has been posted by CRA
# INPUT: A bytes string representing a text file
# OUTPUT: An array of dictionaries for each assessment made
#
from distutils import filelist


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

        # CRA-NO-DATA-RESPONSE-0023
        if subCode == "0023":
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
            current_application.append({"sin": sin, "year": year, "income": income})
    return results


##
# Write a CRA request file
# INPUT: A dictionary of values to write to the file
# OUTPUT: A string representing a text file
#
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
        family_name = row["family_name"].ljust(30)
        given_name = row["given_name"].ljust(30)
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
