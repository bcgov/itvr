import os
from django.test import SimpleTestCase
from api.services import cra


class TestCra(SimpleTestCase):
    # Test against cra in file 00007
    def test_write_in_00007(self):
        data = [
            {
                "sin": "270300379",
                "year": "2020",
                "given_name": "Alice",
                "family_name": "Solange",
                "birth_date": "1971-01-22",
            },
            {
                "sin": "302435839",
                "year": "2020",
                "given_name": "Wendy",
                "family_name": "Turner",
                "birth_date": "1978-05-21",
            },
            {
                "sin": "129922258",
                "year": "2020",
                "given_name": "Lily",
                "family_name": "Redding",
                "birth_date": "1983-07-07",
            },
        ]

        file_contents = cra.write(
            data,
            today="20220516",
            program_code="BCVR",
            cra_env="A",
            cra_sequence="00007",
        )

        cra_in_file_00007_filename = os.path.join(
            os.path.dirname(__file__),
            "cra_in_out",
            "in",
            "TO.ATO#@@00.R7005.IN.BCVR.A00007",
        )
        cra_in_file_00007 = open(cra_in_file_00007_filename).read()

        # Check file contents are exactly equal.
        self.assertEqual(file_contents, cra_in_file_00007)


# data = [{
#   'sin': '270300379',
#   'year': '2020',
#   'given_name': 'Alice',
#   'family_name': 'Solange',
#   'birth_date': '1971-01-22'
# },{
#   'sin': '280671421',
#   'year': '2020',
#   'given_name': 'Nancy',
#   'family_name': 'Durham',
#   'birth_date': '1965-02-17'
# },{
#   'sin': '302435839',
#   'year': '2020',
#   'given_name': 'Wendy',
#   'family_name': 'Turner',
#   'birth_date': '1978-05-21'
# },{
#   'sin': '549713485',
#   'year': '2020',
#   'given_name': 'Patty',
#   'family_name': 'Sullivan',
#   'birth_date': '1994-05-29'
# },{
#   'sin': '127544609', # Not in province
#   'year': '2020',
#   'given_name': 'Yvette',
#   'family_name': 'Stone',
#   'birth_date': '1984-11-16'
# },{
#   'sin': '129922258', # Not filed
#   'year': '2020',
#   'given_name': 'Lily',
#   'family_name': 'Redding',
#   'birth_date': '1983-07-07'
# }]
