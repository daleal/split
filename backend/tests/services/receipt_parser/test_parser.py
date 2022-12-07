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
        parsed = search("1000 hot dog")
        assert_values(parsed, {"description": "hot dog", "full_price": 1000})

    def test_description_price(self):
        parsed = search("hot dog 1000")
        assert_values(parsed, {"description": "hot dog", "full_price": 1000})

    def test_low_price_high_price_description(self):
        parsed = search("1000 2000 hot dog")
        assert_values(parsed, {"description": "hot dog", "full_price": 2000})

    def test_description_low_price_high_price(self):
        parsed = search("hot dog 1000 2000")
        assert_values(parsed, {"description": "hot dog", "full_price": 2000})

    def test_high_price_low_price_description(self):
        parsed = search("2000 1000 hot dog")
        assert_values(parsed, {"description": "hot dog", "full_price": 2000})

    def test_description_high_price_low_price(self):
        parsed = search("hot dog 2000 1000")
        assert_values(parsed, {"description": "hot dog", "full_price": 2000})


class TestAmountPriceOnlyTextDescriptionSearch:
    def test_amount_description_price(self):
        parsed = search("3 hot dog 1000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 1000}
        )

    def test_price_description_amount(self):
        parsed = search("1000 hot dog 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 1000}
        )

    def test_description_amount_price(self):
        parsed = search("hot dog 3 1000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 1000}
        )

    def test_description_price_amount(self):
        parsed = search("hot dog 1000 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 1000}
        )

    def test_amount_description_low_price_high_price(self):
        parsed = search("3 hot dog 1000 2000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_low_price_high_price_description_amount(self):
        parsed = search("1000 2000 hot dog 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_description_amount_low_price_high_price(self):
        parsed = search("hot dog 3 1000 2000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_description_low_price_high_price_amount(self):
        parsed = search("hot dog 1000 2000 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_amount_description_high_price_low_price(self):
        parsed = search("3 hot dog 2000 1000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_high_price_low_price_description_amount(self):
        parsed = search("2000 1000 hot dog 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_description_amount_high_price_low_price(self):
        parsed = search("hot dog 3 2000 1000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )

    def test_description_high_price_low_price_amount(self):
        parsed = search("hot dog 2000 1000 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog", "full_price": 2000}
        )


class TestAmountPriceSearch:  # pylint: disable=too-many-public-methods
    def test_amount_description_number_price(self):
        parsed = search("3 hot dog 1 1000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 1000}
        )

    def test_amount_number_description_price(self):
        parsed = search("3 1 hot dog 1000")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 1000}
        )

    def test_price_description_number_amount(self):
        parsed = search("1000 hot dog 1 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 1000}
        )

    def test_price_number_description_amount(self):
        parsed = search("1000 1 hot dog 3")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 1000}
        )

    def test_description_number_amount_price(self):
        parsed = search("hot dog 1 3 1000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 1000}
        )

    def test_number_description_amount_price(self):
        parsed = search("1 hot dog 3 1000")
        assert_values(
            parsed, {"amount": 1, "description": "hot dog 3", "full_price": 1000}
        )

    def test_description_number_price_amount(self):
        parsed = search("hot dog 1 1000 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 1000}
        )

    def test_number_description_price_amount(self):
        parsed = search("1 hot dog 1000 3")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 1000}
        )

    def test_amount_description_number_low_price_high_price(self):
        parsed = search("3 hot dog 1 1000 2000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_amount_number_description_low_price_high_price(self):
        parsed = search("3 1 hot dog 1000 2000")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    def test_low_price_high_price_description_number_amount(self):
        parsed = search("1000 2000 hot dog 1 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_low_price_high_price_number_description_amount(self):
        parsed = search("1000 2000 1 hot dog 3")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    def test_description_number_amount_low_price_high_price(self):
        parsed = search("hot dog 1 3 1000 2000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_number_description_amount_low_price_high_price(self):
        parsed = search("1 hot dog 3 1000 2000")
        assert_values(
            parsed, {"amount": 1, "description": "hot dog 3", "full_price": 2000}
        )

    def test_description_number_low_price_high_price_amount(self):
        parsed = search("hot dog 1 1000 2000 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_number_description_low_price_high_price_amount(self):
        parsed = search("1 hot dog 1000 2000 3")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    def test_amount_description_number_high_price_low_price(self):
        parsed = search("3 hot dog 1 2000 1000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_amount_number_description_high_price_low_price(self):
        parsed = search("3 1 hot dog 2000 1000")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    def test_high_price_low_price_description_number_amount(self):
        parsed = search("2000 1000 hot dog 1 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_high_price_low_price_number_description_amount(self):
        parsed = search("2000 1000 1 hot dog 3")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )

    def test_description_number_amount_high_price_low_price(self):
        parsed = search("hot dog 1 3 2000 1000")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_number_description_amount_high_price_low_price(self):
        parsed = search("1 hot dog 3 2000 1000")
        assert_values(
            parsed, {"amount": 1, "description": "hot dog 3", "full_price": 2000}
        )

    def test_description_number_high_price_low_price_amount(self):
        parsed = search("hot dog 1 2000 1000 3")
        assert_values(
            parsed, {"amount": 3, "description": "hot dog 1", "full_price": 2000}
        )

    def test_number_description_high_price_low_price_amount(self):
        parsed = search("1 hot dog 2000 1000 3")
        assert_values(
            parsed, {"amount": 3, "description": "1 hot dog", "full_price": 2000}
        )
