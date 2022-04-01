from django.test import TestCase
from api.services.cra import write, read

class TestCra(TestCase):
  # Test the CRA write function
  def test_write(self):
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

    lines = file.split('\n') # Split the file into lines
    lines.pop() # Remove the last line (the terminating character)

    # 4 lines in the file
    self.assertEqual(len(lines), 4)

    # There should be header
    self.assertTrue(lines[0].startswith('7100'))
    self.assertTrue(lines[0].endswith('0'))

    # There should be footer
    self.assertTrue(lines[3].startswith('7102'))
    self.assertTrue(lines[3].endswith('0'))

    # There should two records
    self.assertTrue(lines[1].startswith('7101'))
    self.assertTrue(lines[1].endswith('0'))
    self.assertTrue(lines[2].startswith('7101'))
    self.assertTrue(lines[2].endswith('0'))

    # Test the CRA read function
  def test_read(self):
    # Sample file
    f = open('api/tests/data/EMLI_RESPONSE_FILE_example.txt','r') 
    data = read(f) # Extract our values
    sin = data[0].get('sin')
    income = data[0].get('income')
    year = data[0].get('year')

    # Test the values we care about
    self.assertEqual(sin, '123456789')
    self.assertEqual(income, '30257')
    self.assertEqual(year, '2020')