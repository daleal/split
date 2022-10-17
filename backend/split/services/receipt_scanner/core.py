import re

from receipt_scanner import scan
from receipt_scanner.image.errors import NoContourFoundError

from split.services.receipt_scanner.regular_expressions import search


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


def extract_relevant_information(image_location: str) -> list[dict[str, str | int]]:
    scanned_text = scan(image_location=image_location)
    clean_text = list(
        filter(
            lambda stripped_text: stripped_text != "",
            map(clean_string, scanned_text),
        )
    )
    filtered = [x for x in map(search, clean_text) if x is not None]
    if not filtered:
        raise NoContourFoundError()
    return filtered
