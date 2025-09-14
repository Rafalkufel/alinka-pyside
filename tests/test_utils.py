from datetime import date

import pytest

from alinka.utils import pesel_to_date_of_birth, validate_pesel


class TestValidatePesel:
    @pytest.mark.parametrize(
        "pesel",
        [
            "44051401359",
            "07290423766",
            "02070803628",
        ],
    )
    def test_validate_pesel__valid_pesel(self, pesel):
        assert validate_pesel(pesel)

    @pytest.mark.parametrize(
        "pesel",
        [
            "44051401358",  # Invalid checksum
            "1234567890",  # Too short
            "83010412345",
            "99022912345",
            "88888888888",  # Invalid date
            "abcdefghijk",  # Non-digit characters
            "123456789012",  # Too long
            "",  # Empty string
        ],
    )
    def test_validate_pesel__invalid_pesel(self, pesel):
        assert not validate_pesel(pesel)


class TestPeselToDateOfBirth:
    @pytest.mark.parametrize(
        "pesel, expected_date",
        [
            ("40301362951", date(2040, 10, 13)),
            ("39251058614", date(2039, 5, 10)),
            ("14230216474", date(2014, 3, 2)),
            ("39280845434", date(2039, 8, 8)),
            ("09321992876", date(2009, 12, 19)),
            ("05212294647", date(2005, 1, 22)),
        ],
    )
    def test_pesel_to_date_of_birth__success(self, pesel, expected_date):
        assert validate_pesel(pesel)
        assert pesel_to_date_of_birth(pesel) == expected_date
