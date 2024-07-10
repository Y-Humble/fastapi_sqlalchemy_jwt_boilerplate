def camel_case_to_snake_case(raw_str: str) -> str:
    """
    >>> camel_case_to_snake_case("SomeSHIT")
    'some_shit'
    """
    chars = []
    for c_idx, char in enumerate(raw_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            flag = nxt_idx >= len(raw_str) or raw_str[nxt_idx].isupper()
            prev_char = raw_str[c_idx - 1]

            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")

        chars.append(char.lower())
    return "".join(chars)
