# Test creation of a CRA request file
# Assuming you are currently in the directory `django/api/services/test`...
# To run this test do the following.
# ```bash
# cd ..
# python3 -m test.cra_write
# ```
from cra import write

data = [{
  'sin': '270300379',
  'year': '2020',
  'given_name': 'Alice',
  'family_name': 'Solange',
  'birth_date': '1971-01-22'
},{
  'sin': '280671421',
  'year': '2020',
  'given_name': 'Nancy',
  'family_name': 'Durham',
  'birth_date': '1965-02-17'
},{
  'sin': '302435839',
  'year': '2020',
  'given_name': 'Wendy',
  'family_name': 'Turner',
  'birth_date': '1978-05-21'
},{
  'sin': '549713485',
  'year': '2020',
  'given_name': 'Patty',
  'family_name': 'Sullivan',
  'birth_date': '1994-05-29'
},{
  'sin': '127544609', # Not in province
  'year': '2020',
  'given_name': 'Yvette',
  'family_name': 'Stone',
  'birth_date': '1984-11-16'
},{
  'sin': '129922258', # Not filed 
  'year': '2020',
  'given_name': 'Lily',
  'family_name': 'Redding',
  'birth_date': '1983-07-07'
}]

file = write(data)
print(file, end='')