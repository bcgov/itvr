##
# Read a text file that has been posted by CRA
# INPUT: A string representing a text file
# OUTPUT: An array of dictionaries for each assessment made
#
def read(file):
  results = [] # Array to return
  for line in file: 
    subCode = line[17:21] # Grab the sub-code, defining type of record.
    if subCode != '0236': continue # If not a income entry.... pass.

    # All rows have a set number of spaces for each value
    sin = line[4:13]
    year = line[13:17]
    income = line[21:30].lstrip("0")
    results.append({'sin':sin,'year':year,'income':income}) # Add to array
  return results # Return results
