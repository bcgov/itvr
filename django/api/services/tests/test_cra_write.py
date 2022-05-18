import os
from django.test import SimpleTestCase
from api.services import cra


class TestCraWrite(SimpleTestCase):
    # Test against cra in file 00007
    def test_write_in_00007(self):
        data = [
            {
                "sin": "270300379",
                "years": [2020],
                "given_name": "Alice",
                "family_name": "Solange",
                "birth_date": "19710122",
                "application_id": "1234",
            },
            {
                "sin": "302435839",
                "years": [2020],
                "given_name": "Wendy",
                "family_name": "Turner",
                "birth_date": "19780521",
                "application_id": "1234",
            },
            {
                "sin": "129922258",
                "years": [2020],
                "given_name": "Lily",
                "family_name": "Redding",
                "birth_date": "19830707",
                "application_id": "1234",
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

    # Test against cra in file 00008
    def test_write_in_00008(self):
        data = [
            {
                "sin": "280671421",
                "years": [2020],
                "given_name": "Nancy",
                "family_name": "Durham",
                "birth_date": "19650217",
                "application_id": "ctW8gU57YX4xfQ9o",
            },
            {
                "sin": "270300379",
                "years": [2020],
                "given_name": "Alice",
                "family_name": "Solange",
                "birth_date": "19710122",
                "application_id": "9uXLvNQS5vkKnscD",
            },
            {
                "sin": "549713485",
                "years": [2020],
                "given_name": "Patty",
                "family_name": "Sullivan",
                "birth_date": "19940529",
                "application_id": "B5t92XeH7NnFUwxc",
            },
            {
                "sin": "302435839",
                "years": [2020],
                "given_name": "Wendy",
                "family_name": "Turner",
                "birth_date": "19780521",
                "application_id": "B5t92XeH7NnFUwxc",
            },
        ]

        file_contents = cra.write(
            data,
            today="20220517",
            program_code="BCVR",
            cra_env="A",
            cra_sequence="00008",
        )

        cra_in_file_00008_filename = os.path.join(
            os.path.dirname(__file__),
            "cra_in_out",
            "in",
            "TO.ATO#@@00.R7005.IN.BCVR.A00008",
        )
        cra_in_file_00008 = open(cra_in_file_00008_filename).read()

        # Check file contents are exactly equal.
        self.assertEqual(file_contents, cra_in_file_00008)
