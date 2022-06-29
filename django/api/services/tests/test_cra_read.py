import os
from django.test import SimpleTestCase
from api.services import cra


class TestCraRead(SimpleTestCase):
    # Test against response file 00007
    def test_read_out_00007(self):
        cra_out_file_00007_filename = os.path.join(
            os.path.dirname(__file__),
            "cra_in_out",
            "out",
            "ABCVR00007",
        )

        with open(cra_out_file_00007_filename, "r") as cra_out_file_00007:
            data = cra.read(cra_out_file_00007.read())
            self.assertDictEqual(
                data,
                {
                    "1234            ": [
                        {"sin": "270300379", "year": "2020", "income": "81830"},
                        {"sin": "302435839", "year": "2020", "income": "85687"},
                        {"sin": "129922258", "year": "2020", "income": None},
                    ]
                },
            )

    # Test against response file 00008
    def test_read_out_00008(self):
        cra_out_file_00008_filename = os.path.join(
            os.path.dirname(__file__),
            "cra_in_out",
            "out",
            "ABCVR00008",
        )

        with open(cra_out_file_00008_filename, "r") as cra_out_file_00008:
            data = cra.read(cra_out_file_00008.read())
            self.assertDictEqual(
                data,
                {
                    "ctW8gU57YX4xfQ9o": [
                        {"sin": "280671421", "year": "2020", "income": "53619"}
                    ],
                    "9uXLvNQS5vkKnscD": [
                        {"sin": "270300379", "year": "2020", "income": "81830"}
                    ],
                    "B5t92XeH7NnFUwxc": [
                        {"sin": "549713485", "year": "2020", "income": "28559"},
                        {"sin": "302435839", "year": "2020", "income": "85687"},
                    ],
                },
            )

    # Test against response file 00009
    def test_read_out_00009(self):
        cra_out_file_00009_filename = os.path.join(
            os.path.dirname(__file__),
            "cra_in_out",
            "out",
            "ABCVR00009",
        )

        with open(cra_out_file_00009_filename, "r") as cra_out_file_00009:
            data = cra.read(cra_out_file_00009.read())
            self.assertDictEqual(
                data,
                {
                    "FezRPbX9UGB5S9s2": [
                        {"sin": "130692544", "year": "2020", "income": None}
                    ],
                    "5G7TgFfR2c9Gckur": [
                        {"sin": "130692544", "year": "2020", "income": None},
                        {"sin": "130692544", "year": "2020", "income": None},
                    ],
                },
            )
