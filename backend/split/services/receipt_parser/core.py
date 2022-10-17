import re

from split.errors import NoRelevantItemsFoundError
from split.services.receipt_parser.regular_expressions import search


def clean_string(string: str) -> str:
    return (
        re.sub(r"[0-9]{7,}", "", string)
        .replace(".", "")
        .replace(",", "")
        .replace("$", "")
        .replace("/", "")
        .replace("|", " ")
        .replace("-", " ")
        .strip()
    )


def extract_relevant_information(
    raw_text_lines: list[str],
) -> list[dict[str, str | int]]:
    clean_text = list(
        filter(
            lambda clean_text: clean_text != "",
            map(clean_string, raw_text_lines),
        )
    )
    filtered = [x for x in map(search, clean_text) if x is not None]
    if not filtered:
        raise NoRelevantItemsFoundError()
    return filtered
