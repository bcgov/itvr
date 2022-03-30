# Test creation of a CRA request file
# Assuming you are currently in the directory `django/api/services/test`...
# To run this test do the following.
# ```bash
# cd ..
# python3 -m test.cra_write
# ```
from cra import write

data = {
  'sin': '123456789',
  'year': '2020',
  'given_name': 'John',
  'family_name': 'Smith'
}

file = write(data)
print(file)