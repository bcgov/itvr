from datetime import date


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
        print("LINE")
        print(line)
        # Grab the sub-code, defining type of record.
        subCode = line[17:21]
        print("subCode")
        print(subCode)

        # subcode 0236 is for income
        if subCode != b"0236":
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
def write(data):
    file = ""  # String to return

    today = date.today().strftime("%Y%m%d")  # Get today's date

    # Number of records to write.
    l = str(len(data) + 2)  # Includes header and footer.
    records = "0" * (8 - len(l)) + l

    ####################### Write the header ##############################
    file += "7100"  # Request transaction code
    file += " " * 24  # Blank space

    file += today  #
    file += " "  # Blank space

    file += "BCVRA00009"  # Requesting institution code TODO: make this dynamic

    file += " " * 99  # Blank space

    file += "0\n"  # Blank space

    ####################### Write the body ##############################
    for row in data:
        file += "7101"  # Request transaction code
        file += row["sin"]  # SIN
        file += " " * 4  # Blank space
        file += "0020"  # Sub-code
        file += row["family_name"]  # Family name

        file += " " * (30 - len(row["family_name"]))  # Blank space
        file += row["given_name"]  # Given name

        file += " " * (30 - len(row["given_name"]))  # Blank space
        file += row["birth_date"].replace("-", "")  # Birth date

        file += row["year"]  # Year
        file += " " * 16  # Blank space

        file += "BCVR"  # Program area code
        file += "1234"  # Record identification number (optional)

        file += " " * 29  # Blank space
        file += "0\n"  # Delimiter

    ####################### Write the trailer ###########################
    file += "7102"  # Request transaction code
    file += " " * 24  # Blank space

    file += today  # Request date
    file += " "  # Blank space

    file += "BCVRA00009"  # Requesting institution code TODO: make this dynamic

    file += " " * 6  # Blank space

    file += records  # Number of records in file

    file += " " * 85  # Blank space

    file += "0"  # terminating character

    ####################### Return the file ##############################
    return file
