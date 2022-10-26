def detect_as_word(pattern: str) -> str:
    start_pattern = r"(^|\s+)"
    end_pattern = r"($|\s+)"
    return start_pattern + pattern + end_pattern
