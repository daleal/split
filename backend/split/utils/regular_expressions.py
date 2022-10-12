import re

DENY_LIST = ["total", "credito", "crédito", "debito", "débito", "tarjeta", "fecha"]

DENY_LIST_EXPRESSION = re.compile("|".join(DENY_LIST), re.IGNORECASE)

DESCRIPTION_EXPRESSION_FRAGMENT = (
    r"(?P<description>[a-zA-Z][a-zA-Z0-9 ]{3,}[a-zA-Z0-9])"
)
AMOUNT_EXPRESSION_FRAGMENT = r"(?P<amount>[0-9]{1,3})"
FULL_PRICE_EXPRESSION_FRAGMENT = r"(?P<full_price>[0-9]{4,6})"
SEPARATOR = r"\s+"

ALL_PRESENT_EXPRESSION_VARIANT_1 = re.compile(
    f"{DESCRIPTION_EXPRESSION_FRAGMENT}{SEPARATOR}{AMOUNT_EXPRESSION_FRAGMENT}"
    f"{SEPARATOR}{FULL_PRICE_EXPRESSION_FRAGMENT}"
)

ALL_PRESENT_EXPRESSION_VARIANT_2 = re.compile(
    f"{DESCRIPTION_EXPRESSION_FRAGMENT}{SEPARATOR}{FULL_PRICE_EXPRESSION_FRAGMENT}"
    f"{SEPARATOR}{AMOUNT_EXPRESSION_FRAGMENT}"
)

ALL_PRESENT_EXPRESSION_VARIANT_3 = re.compile(
    f"{AMOUNT_EXPRESSION_FRAGMENT}{SEPARATOR}{DESCRIPTION_EXPRESSION_FRAGMENT}"
    f"{SEPARATOR}{FULL_PRICE_EXPRESSION_FRAGMENT}"
)

ALL_PRESENT_EXPRESSION_VARIANT_4 = re.compile(
    f"{AMOUNT_EXPRESSION_FRAGMENT}{SEPARATOR}{FULL_PRICE_EXPRESSION_FRAGMENT}"
    f"{SEPARATOR}{DESCRIPTION_EXPRESSION_FRAGMENT}"
)

ALL_PRESENT_EXPRESSION_VARIANT_5 = re.compile(
    f"{FULL_PRICE_EXPRESSION_FRAGMENT}{SEPARATOR}{DESCRIPTION_EXPRESSION_FRAGMENT}"
    f"{SEPARATOR}{AMOUNT_EXPRESSION_FRAGMENT}"
)

ALL_PRESENT_EXPRESSION_VARIANT_6 = re.compile(
    f"{FULL_PRICE_EXPRESSION_FRAGMENT}{SEPARATOR}{AMOUNT_EXPRESSION_FRAGMENT}"
    f"{SEPARATOR}{DESCRIPTION_EXPRESSION_FRAGMENT}"
)

AMOUNT_MISSING_VARIANT_1 = re.compile(
    f"{DESCRIPTION_EXPRESSION_FRAGMENT}{SEPARATOR}{FULL_PRICE_EXPRESSION_FRAGMENT}"
)

AMOUNT_MISSING_VARIANT_2 = re.compile(
    f"{FULL_PRICE_EXPRESSION_FRAGMENT}{SEPARATOR}{DESCRIPTION_EXPRESSION_FRAGMENT}"
)

FULL_PRICE_MISSING_VARIANT_1 = re.compile(
    f"{DESCRIPTION_EXPRESSION_FRAGMENT}{SEPARATOR}{AMOUNT_EXPRESSION_FRAGMENT}"
)

FULL_PRICE_MISSING_VARIANT_2 = re.compile(
    f"{AMOUNT_EXPRESSION_FRAGMENT}{SEPARATOR}{DESCRIPTION_EXPRESSION_FRAGMENT}"
)

DESCRIPTION_MISSING_VARIANT_1 = re.compile(
    f"{AMOUNT_EXPRESSION_FRAGMENT}{SEPARATOR}{FULL_PRICE_EXPRESSION_FRAGMENT}"
)

DESCRIPTION_MISSING_VARIANT_2 = re.compile(
    f"{FULL_PRICE_EXPRESSION_FRAGMENT}{SEPARATOR}{AMOUNT_EXPRESSION_FRAGMENT}"
)


def search(string: str) -> dict[str, str | int] | None:
    if DENY_LIST_EXPRESSION.search(string):
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
        FULL_PRICE_MISSING_VARIANT_1,
        FULL_PRICE_MISSING_VARIANT_2,
        DESCRIPTION_MISSING_VARIANT_1,
        DESCRIPTION_MISSING_VARIANT_2,
    ]
    for expression in expressions:
        search_result = expression.search(string)
        if search_result is not None:
            raw_result = search_result.groupdict()
            final_result: dict[str, str | int] = {}
            description = raw_result.get("description")
            amount = raw_result.get("amount")
            full_price = raw_result.get("full_price")
            if description:
                final_result = {**final_result, "description": description}
            if amount:
                final_result = {**final_result, "amount": int(amount)}
            if full_price:
                final_result = {**final_result, "full_price": int(full_price)}
            return final_result
    return None
