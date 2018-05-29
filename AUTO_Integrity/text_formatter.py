def format_by_charater_length(max_length: int, text: str):
    """
    Formats a string of text so that it doesn't go past the max length. Breaks the
    string up by adding a return character
    :param max_length: max length of the string
    :param text: text to bring up
    :return: the formatted string
    """
    # split text by " " to find words
    words_in_text = iter(text.split(" "))
    current_length = 0
    previous_word = next(words_in_text)
    next_word = next(words_in_text)
    updated_words = []
    try:
        while True:
            current_length += len(previous_word) + 1  # add one for the space
            if current_length >= max_length:
                previous_word += "\n "
                current_length = 0
            updated_words.append(previous_word)
            previous_word = next_word
            next_word = next(words_in_text)
    except StopIteration:
        updated_words.append(previous_word)

    return """ """.join(updated_words)


def format_by_charater_length_with_keyword(max_length: int, text: str, keyword: str):
    """
    Formats a string of text so that it it begins with a keyword and doesn't go over
    a max length.
    :param max_length: max length of the string.
    :param text: text to format
    :param keyword: keyword to add to string
    :return: formatted string
    """
    # split text by " " to find words
    total_lenth = max_length + len(keyword) + 1 # add one for space after keyword
    words_in_text = iter(text.split(" "))
    current_length = 0
    previous_word = next(words_in_text)
    next_word = next(words_in_text)
    updated_words = []
    try:
        while True:
            current_length += len(previous_word) + 1  # add one for space after word
            if current_length >= total_lenth:
                previous_word += "\n{}".format(keyword)
                current_length = 0
            updated_words.append(previous_word)
            previous_word = next_word
            next_word = next(words_in_text)
    except StopIteration:
        updated_words.append(previous_word)

    # add keyword to first word
    updated_words[0] = "{} ".format(keyword) +  updated_words[0]

    return """ """.join(updated_words)


def main():
    text = "This req file was created by Seth Pitts on 09MAY2018 for ZC1/CHP"

    format_by_charater_length(50, text)
    format_by_charater_length_with_keyword(30, text, "COMMENT")


if __name__ == '__main__':
    main()