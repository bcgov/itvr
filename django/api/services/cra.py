##
# Read a text file that has been posted by CRA
# Will have \r\n as it's from a Windows machine
# INPUT: A bytes string representing a text file
# OUTPUT: An array of dictionaries for each assessment made
#
def read(file):
    print(file)
    results = []
    for line in file.split(b"\r\n"):
        print(line)
        # Grab the sub-code, defining type of record.
        subCode = line[17:21]

        # From Susan:
        # The business folks did flip flop on the net income
        # (record 0236) line 23600 vs total income (0150)
        # but total income (record 0150) or line 15000 was the final decision.
        # subcode 0236 is for income
        if subCode == b"0236":
            sin = line[4:13]
            year = line[13:17]
            income = line[21:30].lstrip(b"0")
            results.append({"sin": sin, "year": year, "income": income})
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
        file += "7101"  # Request transaction code
        file += row["sin"]  # SIN
        file += " " * 4  # Blank space
        file += "0020"  # Sub-code
        file += row["family_name"]  # Family name

        file += " " * (30 - len(row["family_name"]))  # Blank space
        file += row["given_name"]  # Given name

        file += " " * (30 - len(row["given_name"]))  # Blank space
        file += row["birth_date"]  # Birth date

        file += row["year"]  # Year
        file += " " * 16  # Blank space

        file += program_code
        file += row["application_id"]  # Record identification number (optional)

        file += " " * 29  # Blank space
        file += "0\n"  # Delimiter

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
