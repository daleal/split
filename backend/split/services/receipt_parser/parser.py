import re

from split.services.receipt_parser.utils import detect_as_word

DENIED_WORDS_LIST = [
    "balance",
    "cliente",
    "consumo",
    "credito",
    "debito",
    "descuento",
    "dscto",
    "fecha",
    "iva",
    "local",
    "monto",
    "neto",
    "propina",
    "sugerida",
    "tarjeta",
    "tienda",
    "total",
]

DENIED_WORDS_EXPRESSION = re.compile(
    detect_as_word("|".join(DENIED_WORDS_LIST)),
    re.IGNORECASE
)

DESCRIPTION_EXPRESSION_FRAGMENT = (
    r"(?P<description>\d* ?[a-zA-Z\(\)][a-zA-Z0-9 \(\)]+[a-zA-Z\(\)])"
)
AMOUNT_EXPRESSION_FRAGMENT = r"(?P<amount>[0-9]{1,2})"
FULL_PRICE_EXPRESSION_FRAGMENT = (
    r"((?P<price_1>[0-9]{3,6})(\s+(?P<price_2>[0-9]{3,6}))?)"
)
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
            price_1 = int(raw_result["price_1"])
            price_2 = int(raw_result["price_2"] or "0")
            full_price = max(price_1, price_2)
            if full_price < 100:
                return None
            final_result: dict[str, str | int] = {
                "description": raw_result["description"],
                "full_price": full_price,
            }
            amount = raw_result.get("amount")
            if amount:
                final_result = {**final_result, "amount": int(amount)}
            return final_result
    return None
