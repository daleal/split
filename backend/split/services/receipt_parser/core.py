from split.errors import NoRelevantItemsFoundError
from split.services.receipt_parser.cleaner import clean_string
from split.services.receipt_parser.parser import search


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
