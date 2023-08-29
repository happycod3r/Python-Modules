# strings.py

def contains(char: str, string: str):
    # Remove leading and trailng space if any
    if char.startswith(" "):
        char = char.lstrip(" ")
    if char.endswith(" "):
        char = char.rstrip(" ")
    # Get the length of the chars to match
    char_len = len(char)
    previous_char = None
    # If we're only matching one character we don't need to do much
    if char_len == 1:
        return char in string
    # If we have to match more than one character we need to 
    # keep track of the order of matches to make sure they are 
    # consecutive. ie. 
    #   if we have a string: "I love coding"
    #   and we want to match "love" then we need to make sure
    #   "l", "o", "v", and "e" are in a row for an actual match
    #   otherwise you could write "lovre" and it will still match
    #   which is not good or really a match
    elif char_len > 1:
        str_match = [] # Stores each character that matches
        index = 0
        for i in range(char_len):
            for j in range(len(string)):
                # Store the previous character and use it to assure that the
                # matches are consecutive and there is no break in the sequence
                previous_char = char[i - 1]
                # If we are currently matching the first character in the sequence,
                # then there is no previous character and it should just be appended
                # if found to be a match
                if index == 0:
                    if char[i] == string[j]:
                        str_match.append(char[i])
                        continue
                # If we are beyond the first character in the sequence then 
                # we need to check to make sure that the previous character
                # was also a match to move on. If the previous characters 
                # didn't match then there was a break in the sequence therefore
                # signaling that there isn't a consecutive match yet
                if char[i] == string[j] and previous_char == string[j - 1]:
                    str_match.append(char[i])
        # Lastly as a precaution we check if the matched string is 
        # the correct length by comparing to the length of char.
        if len(str_match) == char_len:
            # Reconstruct the string to reverse it.
            reconstructed = ""
            for i in range(0, len(str_match)):
                reconstructed = reconstructed + str_match[i]
            if reconstructed == char:
                return True
    return False