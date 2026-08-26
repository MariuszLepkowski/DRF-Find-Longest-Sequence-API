def find_longest_sequence(s: str | None) -> str:
    if not s:
        return ""

    current_length = max_length = 1
    current_start = best_start = 0

    for index in range(1, len(s)):
        if s[index] == s[index - 1]:
            current_length += 1

            if current_length > max_length:
                max_length = current_length
                best_start = current_start
        else:
            current_length = 1
            current_start = index

    return s[best_start : best_start + max_length]
