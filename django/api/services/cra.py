from datetime import date

##
# Read a text file that has been posted by CRA
# INPUT: A string representing a text file
# OUTPUT: An array of dictionaries for each assessment made
#
def read(file):
  results = [] # Array to return
  for line in file: 
    subCode = line[17:21] # Grab the sub-code, defining type of record.
    if subCode != '0236': continue # If not an income entry.... pass.

    # All rows have a set number of spaces for each value
    sin = line[4:13]
    year = line[13:17]
    income = line[21:30].lstrip("0")
    results.append({'sin':sin,'year':year,'income':income}) # Add to array
  return results # Return results

##
# Write a CRA request file
# INPUT: A dictionary of values to write to the file
# OUTPUT: A string representing a text file
#
def write(data):
  file = "" # String to return

  today = date.today().strftime("%Y%m%d") # Get today's date

  ####################### Write the header ##############################
  file += '7100' # Request transaction code
  file += ' ' * 24 # Blank space

  file += today # 
  file += ' ' # Blank space

  file += 'BCGSP00521' # Requesting institution code TODO: make this dynamic

  file += ' ' * 99 # Blank space

  file += '0\n' # Blank space


  ####################### Write the body ##############################
  for row in data:
    file += '7101' # Request transaction code
    file += row['sin'] # SIN
    file += ' ' * 4 # Blank space
    file += '0020' # Sub-code
    file += row['family_name'] # Family name

    file += ' ' * (30 - len(row['family_name'])) # Blank space
    file += row['given_name'] # Given name

    file += ' ' * (30 - len(row['given_name'])) # Blank space
    file += row['birth_date'].replace('-','') # Birth date

    file += row['year'] # Year
    file += ' ' * 14 # Blank space

    file += 'BCGS' # Program area code
    file += '1234' # Record identification number (optional)

    file += ' ' * 31 # Blank space
    file += '0\n' # Delimiter


  ####################### Write the trailer ###########################
  file += '7102' # Request transaction code 
  file += ' ' * 24 # Blank space

  file += today # Request date
  file += ' ' # Blank space

  file += 'BCGSP00521' # Requesting institution code TODO: make this dynamic

  file += ' ' * 6 # Blank space

  file += '0' * 8 # Number of records in file TODO: make this dynamic

  file += ' ' * 85 # Blank space

  file += '0\n' # terminating character 

  
  ####################### Return the file ##############################
  return file