def RemoveNonAscii(text):
    """
    Keeps only the first 256 characters of extended ASCII. Probably bad for portability
    """
    newString = ""
    for char in text:
        if ord(char) <= 255:
            newString = newString + char
    return newString


def StringOfSpaces(num_spaces):
    """
    Returns a string of spaces, with length equal to spaces parameter
    """
    return "".zfill(num_spaces).replace("0", " ")


def PlaceString(string, length=None, start=0, place_into=None):
    """Places the string specified into an existing string, if specified, otherwise a string of spaces.

    Args:
        string (): The text to place within a string
        length (): The total length of the string, after placement. The output string is guaranteed to not be longer than this. Pass in None to create a string that is as long as needed to place at the specified location.
        start (): The index to start the specified string. Note that this starts at 0
        place_into (): The string to place the string into. Pass None to place into a string of spaces.

    Returns: None on failure, the result string on success
        
    """
    # Calculate the length if not explicitly defined.
    if length is None:
        length = len(string) + start
        if place_into is not None: # Length is max of this string or the place_into string
            length = max(len(place_into),length)

    # Calculates the positive index when a negative index is passed.
    if start < 0:
        start = length + start

    # Post-placement string would exceed the defined length
    if len(string) + start > length:
        return None

    # Ensures that the place_into string is long enough
    if place_into is not None:
        if isinstance(place_into,str):
            if len(place_into) > length: # Would exceed bounds
                return None
            elif len(place_into) < length: # Add extra spaces to the end of place_into if necessary
                place_into = PlaceString(place_into,length)

        # place_into is not a string
        else:
            return None

    # place_into was not defined, so use a string of just spaces.
    else:
        place_into = StringOfSpaces(length)

    # Places the text string into the place_into string.
    s = place_into[:start] + string + place_into[start + len(string) :]
    return s


def CombineStrings(strings,length=None):
    """Combines a list of strings into a single string. Will be as long as necessary or can be capped to a set length

    Args:
        strings (): A list of tuples of (text,index). These are the strings and their locations within the output string
        length (): The maximum length of the output. Pass None to not set any cap

    Returns: None on failure, output string on success
        
    """
    result_string = None
    for string in strings:
        text,start = string
        result_string = PlaceString(text,length,start,result_string)
        # Failure from PlaceString
        if result_string is None:
            return None
    return result_string


def BreakUpString(string,line_length):
    """Breaks up a string into a list of lines, each line at max line_length long

    Args:
        string (): The string to be broken up. Use '\n' within the string to force line breaks.
        line_length (): The max length of any given line.

    Returns: A list of lines, with no newline characters in it. Each element is a single line.
        
    """
    # Splits the string into a list, separating at newlines already present (ends of paragraphs)
    string = string.splitlines()
    tempstr = ""  # Stores the working string while it is being built up
    checkstr = ""  # Used for checking if adding the next word will push the string over the length limit
    tabulatedList = []  # A list comprised of each finished line
    for item in string:
        item = (
            item.split()
        )  # Splits the paragraphs up by words. Separating at every space
        for word in item:  # Loops through every word
            # If the word is longer than the amount of space for a single line
            if len(word) > line_length:
                # Finishes the work in progress line
                tabulatedList.append(f"{checkstr}\n")
                tempstr = ""
                checkstr = ""

                # Used to split the long word (typically links) into multiple lines
                workingWord = word

                # Splits word into line_length sized lines
                while len(workingWord) > line_length:
                    tabulatedList.append(
                        f"{workingWord[:line_length]}\n"
                    )
                    workingWord = workingWord[line_length:]

                # Gives the end of the word (the part less than line_length length) its own line
                tabulatedList.append(f"{workingWord}\n")
                continue

            # For normal words
            checkstr = checkstr + word

            # simply adds new word to tempstr if it won't make it too long
            if len(checkstr) < line_length:  
                tempstr = checkstr
                tempstr = tempstr + " "
                checkstr = tempstr

            # Adds word, then pushes line to list and starts new line
            elif len(checkstr) == line_length:
                tabulatedList.append(f"{checkstr}\n")
                tempstr = ""
                checkstr = ""

            # Pushes current line to list, then starts a new line with word at the start
            else:
                tabulatedList.append(f"{tempstr}\n")
                tempstr = word + " "
                checkstr = tempstr

        # Adds leftover words at the end of paragraph, so long as tempstr is not empty
        if tempstr.strip():
            tabulatedList.append(f"{tempstr}\n")
            tempstr = ""
            checkstr = ""
    return tabulatedList


def Tabulate(string, terminal_width=80, spaces=8, prefix=None):
    """ Given a string, splits the string across enough lines, such that each line
    will fit within the maximum terminal_width specified. Applies a prefix to every single line.

    Args:
        string (): The string to be split across lines. Use '\n' within the string to force line breaks
        terminalWidth (): The maximum length of any line
        spaces (): The number of spaces to prefix each line with. Does nothing if prefix is set.
        prefix (): The string to prefix each line with. Overrides any value in spaces.

    Returns: A string with a newline '\n' character at the end of each line. When the string is printed, the lines will all be of length less than terminal_width
        
    """
    # Removes tabs from the original string
    string = string.replace("\t", "")

    if prefix is not None:
        spaces = len(prefix)

    line_length = terminal_width - spaces  # the number of non-space characters for the line
    tabulatedList = BreakUpString(string,line_length)

    if prefix is None:
        prefix = StringOfSpaces(spaces)
    return prefix + prefix.join(tabulatedList)  # Combines list into a single string


def Enbox(
    stringList,
    terminalWidth,
    leftPadding=1,
    rightPadding=1,
    leftMargin=0,
    rightMargin=0,
    fancy=False,
):
    """
    Draws boxes around content. stringList is a list of strings of content. All entries in the list will be combined
    into the same box. Using "%separator%" as an entry in the list will draw a horizontal line. terminalWidth is the width of the box.
    Padding is the number of spaces between side walls and content.
    Margin is the number of spaces between the edge of terminal and the side walls.
    fancy is whether fancy characters will be used or basic characters.
    """
    boxWidth = terminalWidth - (leftMargin + rightMargin)
    textBoxWidth = boxWidth - (leftPadding + rightPadding)

    topLeft = "+"
    topRight = "+"
    bottomLeft = "+"
    bottomRight = "+"
    sideLeft = "+"
    sideRight = "+"
    vertical = "|"
    horizontal = "-"

    if fancy:
        topLeft = "┌"
        topRight = "┐"
        bottomLeft = "└"
        bottomRight = "┘"
        sideLeft = "├"
        sideRight = "┤"
        vertical = "│"
        horizontal = "─"

    s = []

    # Creates the top border of the box
    s.append(f"{topLeft}{''.zfill(boxWidth - 2).replace('0', horizontal)}{topRight}")

    for item in stringList:  # Loops through each item in the content list.
        if item is not None:
            # Creates a separating line in the box
            if item == "%separator%":
                # Adds a horizontal line
                s.append(
                    f"{sideLeft}{''.zfill(boxWidth - 2).replace('0', horizontal)}{sideRight}"
                )
            else:
                # Breaks the content into lines that will fit in the text box.
                listStrings = Tabulate(item, textBoxWidth - 1, leftPadding).splitlines()
                for line in listStrings:
                    # Adds the side walls and appends the line to the list of lines
                    line = PlaceString(line, textBoxWidth, 0)
                    s.append(f"{vertical}{line}{vertical}")

    # Creates bottom line
    s.append(
        f"{bottomLeft}{''.zfill(boxWidth - 2).replace('0', horizontal)}{bottomRight}"
    )
    return s
