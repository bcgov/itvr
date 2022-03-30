# Test creation of a CRA request file
# Assuming you are currently in the directory `django/api/services/test`...
# To run this test do the following.
# ```bash
# cd ..
# python3 -m test.cra_write
# ```
from cra import write

data = [{
  'sin': '123456789',
  'year': '2020',
  'given_name': 'John',
  'family_name': 'Smith',
  'birth_date': '1955-01-01'
},{
  'sin': '987654321',
  'year': '2020',
  'given_name': 'Amanda',
  'family_name': 'Williams',
  'birth_date': '1965-02-21'
}]

file = write(data)
print(file)