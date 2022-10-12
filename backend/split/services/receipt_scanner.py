from receipt_scanner import scan

from split.utils.regular_expressions import search


def extract_relevant_information(image_location: str) -> list[dict[str, str | int]]:
    scanned_text = scan(image_location=image_location)
    clean_text = list(
        filter(
            lambda stripped_text: stripped_text != "",
            map(lambda raw_text: raw_text.strip(), scanned_text),
        )
    )
    filtered = [x for x in map(search, clean_text) if x is not None]
    if not filtered:
        raise Exception("F")
    return filtered
