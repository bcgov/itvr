# Test loading and interpretting a CRA revenue response
# Assuming you are currently in the directory `django/api/services/test`...
# To run this test do the following.
# ```bash
# cd ..
# python3 -m test.cra_read
# ```
from cra import read

f = open('test/data/EMLI_RESPONSE_FILE_example.txt','r') # Sample file
data = read(f) # Extract our values
sin = data[0].get('sin')
income = data[0].get('income')
year = data[0].get('year')
print(f'SIN:    {sin}')
print(f'Year:   {year}')
print(f'Income: ${income}')