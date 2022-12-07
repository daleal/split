import pytest

from split.services.receipt_parser.parser import search


def assert_values(
    parsed: dict[str, str | int] | None, expected: dict[str, str | int] | None = None
) -> None:
    if parsed is None:
        assert expected is None
    else:
        assert parsed == expected


class TestPriceSearch:
    def test_price_description(self):
        text = "1000 hot dog"
        parsed = search(text)
        assert_values(parsed, {"description": "hot dog", "full_price": 1000})

    def test_description_price(self):
        text = "hot dog 1000"
        parsed = search(text)
        assert_values(parsed, {"description": "hot dog", "full_price": 1000})

    def test_low_price_high_price_description(self):
        text = "1000 2000 hot dog"
        parsed = search(text)
        assert_values(parsed, {"description": "hot dog", "full_price": 2000})

    def test_description_low_price_high_price(self):
        text = "hot dog 1000 2000"
        parsed = search(text)
        assert_values(parsed, {"description": "hot dog", "full_price": 2000})

    def test_high_price_low_price_description(self):
        text = "2000 1000 hot dog"
        parsed = search(text)
        assert_values(parsed, {"description": "hot dog", "full_price": 2000})

    def test_description_high_price_low_price(self):
        text = "hot dog 2000 1000"
        parsed = search(text)
        assert_values(parsed, {"description": "hot dog", "full_price": 2000})


class TestAmountPriceOnlyTextDescriptionSearch:
    def test_amount_description_price(self):
        text = "3 hot dog 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 1000}
        )

    def test_price_description_amount(self):
        text = "1000 hot dog 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 1000}
        )

    def test_description_amount_price(self):
        text = "hot dog 3 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 1000}
        )

    def test_description_price_amount(self):
        text = "hot dog 1000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 1000}
        )

    def test_amount_description_low_price_high_price(self):
        text = "3 hot dog 1000 2000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_low_price_high_price_description_amount(self):
        text = "1000 2000 hot dog 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_description_amount_low_price_high_price(self):
        text = "hot dog 3 1000 2000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_description_low_price_high_price_amount(self):
        text = "hot dog 1000 2000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_amount_description_high_price_low_price(self):
        text = "3 hot dog 2000 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_high_price_low_price_description_amount(self):
        text = "2000 1000 hot dog 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_description_amount_high_price_low_price(self):
        text = "hot dog 3 2000 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_description_high_price_low_price_amount(self):
        text = "hot dog 2000 1000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )


class TestAmountPriceSearch:  # pylint: disable=too-many-public-methods
    @pytest.mark.xfail(reason="Case not implemented")
    def test_amount_description_number_price(self):
        text = "3 hot dog 1 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 1000}
        )

    def test_amount_number_description_price(self):
        text = "3 1 hot dog 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 1000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_price_description_number_amount(self):
        text = "1000 hot dog 1 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 1000}
        )

    def test_price_number_description_amount(self):
        text = "1000 1 hot dog 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 1000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_description_number_amount_price(self):
        text = "hot dog 1 3 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 1000}
        )

    def test_number_description_amount_price(self):
        text = "1 hot dog 3 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 1000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_description_number_price_amount(self):
        text = "hot dog 1 1000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 1000}
        )

    def test_number_description_price_amount(self):
        text = "1 hot dog 1000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 1000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_amount_description_number_low_price_high_price(self):
        text = "3 hot dog 1 1000 2000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_amount_number_description_low_price_high_price(self):
        text = "3 1 hot dog 1000 2000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_low_price_high_price_description_number_amount(self):
        text = "1000 2000 hot dog 1 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_low_price_high_price_number_description_amount(self):
        text = "1000 2000 1 hot dog 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_description_number_amount_low_price_high_price(self):
        text = "hot dog 1 3 1000 2000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_number_description_amount_low_price_high_price(self):
        text = "1 hot dog 3 1000 2000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_description_number_low_price_high_price_amount(self):
        text = "hot dog 1 1000 2000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_number_description_low_price_high_price_amount(self):
        text = "1 hot dog 1000 2000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_amount_description_number_high_price_low_price(self):
        text = "3 hot dog 1 2000 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_amount_number_description_high_price_low_price(self):
        text = "3 1 hot dog 2000 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_high_price_low_price_description_number_amount(self):
        text = "2000 1000 hot dog 1 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_high_price_low_price_number_description_amount(self):
        text = "2000 1000 1 hot dog 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_description_number_amount_high_price_low_price(self):
        text = "hot dog 1 3 2000 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_number_description_amount_high_price_low_price(self):
        text = "1 hot dog 3 2000 1000"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    @pytest.mark.xfail(reason="Case not implemented")
    def test_description_number_high_price_low_price_amount(self):
        text = "hot dog 1 2000 1000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_number_description_high_price_low_price_amount(self):
        text = "1 hot dog 2000 1000 3"
        parsed = search(text)
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )
