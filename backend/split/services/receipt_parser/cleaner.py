import re
from functools import reduce

from unidecode import unidecode

DENIED_PATTERNS_LIST = [
    re.compile(r"(^|\s+)\d{1,2} del? 20\d{2}($|\s+)"),  # human-readable dates
    re.compile(r"(^|\s+)(20)?\d{2}-\d{2}-(20)?\d{2}($|\s+)"),  # dates
    re.compile(r"(^|\s+)(20)?\d{2}/\d{2}/(20)?\d{2}($|\s+)"),  # dates
]

CHARACTERS_TO_REMOVE = [
    ".",
    ",",
    "$",
    "€",
    "¥",
    "¢",
    "'",
    '"',
    "“",
    "”",
    "‘",
    "’",
    "{",
    "}",
    "[",
    "]",
    "¡",
    "!",
    "¿",
    "?",
]
CHARACTERS_TO_REPLACE_WITH_SPACE = [
    "*",
    ":",
    ";",
    "/",
    "\\",
    "|",
    "=",
    "+",
    "_",
    "-",
    "—",
    "<",
    ">",
    "«",
    "»",
    "©",
]

REGEX_TO_REMOVE = re.compile("|".join(re.escape(x) for x in CHARACTERS_TO_REMOVE))
REGEX_TO_REPLACE_WITH_SPACE = re.compile(
    "|".join(re.escape(x) for x in CHARACTERS_TO_REPLACE_WITH_SPACE)
)

CUSTOM_REPLACEMENTS = [
    # dot + space in between only digits to only dot
    lambda text: re.sub(r"((^|\s+)\$?\d+)(\.|,) (\d+)($|\s+)", r"\1\3\4\5", text),
    # two decimals to only integer
    lambda text: re.sub(r"((^|\s+)\d+)(\.|,)\d{1,2}($|\s+)", r"\1\4", text),
]


def clean_string(string: str) -> str:
    for denied_pattern in DENIED_PATTERNS_LIST:
        if denied_pattern.search(string):
            return ""
    custom_replacements = reduce(
        lambda text, replacement: replacement(text),
        CUSTOM_REPLACEMENTS,
        string,
    )
    string_with_no_large_numbers = re.sub(r"[0-9]{7,}", "", custom_replacements)
    string_with_removed_characters = REGEX_TO_REMOVE.sub(
        "",
        string_with_no_large_numbers,
    )
    string_with_replaced_characters = REGEX_TO_REPLACE_WITH_SPACE.sub(
        " ",
        string_with_removed_characters,
    )
    return unidecode(string_with_replaced_characters).strip()
