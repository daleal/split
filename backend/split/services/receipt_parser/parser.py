import re

DENIED_WORDS_LIST = [
    "total",
    "balance",
    "monto",
    "consumo",
    "descuento",
    "credito",
    "crédito",
    "debito",
    "débito",
    "tarjeta",
    "fecha",
    "propina",
    "sugerida",
    "local",
    "tienda",
]

DENIED_WORDS_EXPRESSION = re.compile("|".join(DENIED_WORDS_LIST), re.IGNORECASE)

DESCRIPTION_EXPRESSION_FRAGMENT = (
    r"(?P<description>\d*[a-zA-Z\(\)][a-zA-Z0-9 \(\)]{3,}[a-zA-Z0-9\(\)])"
)
AMOUNT_EXPRESSION_FRAGMENT = r"(?P<amount>[0-9]{1,3})"
FULL_PRICE_EXPRESSION_FRAGMENT = r"(?P<full_price>[0-9]{4,6})"
SEPARATOR = r"\s+"


def generate_expression(*fragments: str) -> re.Pattern:
    return re.compile(f"^{SEPARATOR.join(fragments)}$")


ALL_PRESENT_EXPRESSION_VARIANT_1 = generate_expression(
    DESCRIPTION_EXPRESSION_FRAGMENT,
    AMOUNT_EXPRESSION_FRAGMENT,
    FULL_PRICE_EXPRESSION_FRAGMENT,
)

ALL_PRESENT_EXPRESSION_VARIANT_2 = generate_expression(
    DESCRIPTION_EXPRESSION_FRAGMENT,
    FULL_PRICE_EXPRESSION_FRAGMENT,
    AMOUNT_EXPRESSION_FRAGMENT,
)

ALL_PRESENT_EXPRESSION_VARIANT_3 = generate_expression(
    AMOUNT_EXPRESSION_FRAGMENT,
    DESCRIPTION_EXPRESSION_FRAGMENT,
    FULL_PRICE_EXPRESSION_FRAGMENT,
)

ALL_PRESENT_EXPRESSION_VARIANT_4 = generate_expression(
    AMOUNT_EXPRESSION_FRAGMENT,
    FULL_PRICE_EXPRESSION_FRAGMENT,
    DESCRIPTION_EXPRESSION_FRAGMENT,
)

ALL_PRESENT_EXPRESSION_VARIANT_5 = generate_expression(
    FULL_PRICE_EXPRESSION_FRAGMENT,
    DESCRIPTION_EXPRESSION_FRAGMENT,
    AMOUNT_EXPRESSION_FRAGMENT,
)

ALL_PRESENT_EXPRESSION_VARIANT_6 = generate_expression(
    FULL_PRICE_EXPRESSION_FRAGMENT,
    AMOUNT_EXPRESSION_FRAGMENT,
    DESCRIPTION_EXPRESSION_FRAGMENT,
)

AMOUNT_MISSING_VARIANT_1 = generate_expression(
    DESCRIPTION_EXPRESSION_FRAGMENT,
    FULL_PRICE_EXPRESSION_FRAGMENT,
)

AMOUNT_MISSING_VARIANT_2 = generate_expression(
    FULL_PRICE_EXPRESSION_FRAGMENT,
    DESCRIPTION_EXPRESSION_FRAGMENT,
)


def search(string: str) -> dict[str, str | int] | None:
    if DENIED_WORDS_EXPRESSION.search(string):
        return None
    expressions = [
        ALL_PRESENT_EXPRESSION_VARIANT_1,
        ALL_PRESENT_EXPRESSION_VARIANT_2,
        ALL_PRESENT_EXPRESSION_VARIANT_3,
        ALL_PRESENT_EXPRESSION_VARIANT_4,
        ALL_PRESENT_EXPRESSION_VARIANT_5,
        ALL_PRESENT_EXPRESSION_VARIANT_6,
        AMOUNT_MISSING_VARIANT_1,
        AMOUNT_MISSING_VARIANT_2,
    ]
    for expression in expressions:
        search_result = expression.search(string)
        if search_result is not None:
            raw_result = search_result.groupdict()
            final_result: dict[str, str | int] = {
                "description": raw_result["description"],
                "full_price": int(raw_result["full_price"]),
            }
            amount = raw_result.get("amount")
            if amount:
                final_result = {**final_result, "amount": int(amount)}
            return final_result
    return None
