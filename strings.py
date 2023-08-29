# string_module

def contains(char: str, string: str):
    """
    Returns True if the character or sequence of characters represented 
    by char is a substring of string. Returns False otherwise.
    """
    if char.startswith(" "):
        char = char.lstrip(" ")
    if char.endswith(" "):
        char = char.rstrip(" ")
    char_len = len(char)
    previous_char = None
    if char_len == 1:
        return char in string
    elif char_len > 1:
        str_match = []
        index = 0
        for i in range(char_len):
            for j in range(len(string)):
                previous_char = char[i - 1]
                if index == 0:
                    if char[i] == string[j]:
                        str_match.append(char[i])
                        continue
                if char[i] == string[j] and previous_char == string[j - 1]:
                    str_match.append(char[i])
        if len(str_match) == char_len:
            reconstructed = ""
            for i in range(0, len(str_match)):
                reconstructed = reconstructed + str_match[i]
            if reconstructed == char:
                return True
    return False
  