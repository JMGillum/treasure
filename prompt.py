from datetime import datetime
from enum import Enum


def IsYes(string):
    """Checks whether a string is equivalent to 'yes' or a confirmation

    Args:
        string (): The string to be checked.

    Returns: True if it is equivalent to yes, otherwise False.
        
    """
    string = string.strip().lower()
    return string == 'y' or string == "yes"


def IsNo(string):
    """Checks whether a string is equivalent to 'no' or a decline.

    Args:
        string (): The string to be checked.

    Returns: True if it is equivalent to no, otherwise False.
        
    """
    string = string.strip().lower()
    return string == 'n' or string == "no"


def GetConfirmation(prompt):
    """Prompts the user to confirm yes or no to the provided prompts. Loops until valid input is entered.

    Args:
        prompt (): The text that will be displayed to prompt for yes or no.

    Returns: True/False corresponding to yes/no
        
    """
    while True:
        response = input(f"{prompt} (y/n): ")
        if IsYes(response):
            return True
        elif IsNo(response):
            return False
        else:
            print("You must enter either 'y' or 'n'.")


def GetDate(return_datetime=False,return_str_format="%Y-%m-%d"):
    """Prompts the user to enter a date. Continuing in a loop until a valid date is entered.

    Args:
        return_datetime (): Pass True to return a datetime object. Pass False to return a formatted string.
        return_str_format (): If return_datetime is False, this is the format string that the date will be formatted to for return.

    Returns: Either datetime object or formatted string of date.
        
    """
        
    date_prompt = "Enter date as either: 'D.M.Y', 'M/D/Y', or 'Y-M-D': "
    found_date = None
    response = None

    # Various states for controlling logic.
    State = Enum("state",[("CONFIRM_STATE",0),("INPUT_STATE",1),("VALIDATE_STATE",2),("SUCCESS_STATE",3)])
    current_state = State.INPUT_STATE
    while not current_state == State.SUCCESS_STATE:

        # Prompts the user to enter a date.
        if current_state == State.INPUT_STATE:
            response = input(date_prompt)
            if response:
                current_state = State.VALIDATE_STATE

        # Gets confirmation for date input
        if current_state == State.CONFIRM_STATE:
            response = input(f'Press enter to accept {found_date.strftime("%d %B %Y")} or {date_prompt}')
            # User confirmed the date by not entering a new one.
            if not response:
                current_state = State.SUCCESS_STATE
                break
            # User entered a new date, so validate
            current_state = State.VALIDATE_STATE

        # Validates that the input is a valid date.
        if current_state == State.VALIDATE_STATE:
            # No input to validate, so get new input.
            if not response:
                current_state = State.INPUT_STATE


            # Checks which of the three formats was used. The one used correctly
            # will have three elements when split on the seperator.
            # Ex: '20.5.2023'.split('.') = [20,5,2023],

            # Stores a tuple of (year,month,day) if a date format is correctly used.
            # So long as this value is None, no format has been correctly used.
            date = None

            # Attempts to split along '.'
            delimited_response = response.split(".")
            if len(delimited_response) == 3:
                date = (delimited_response[2],delimited_response[1],delimited_response[0])

            # Attempts to split along '/'
            if date is None:
                delimited_response = response.split("/")
                if len(delimited_response) == 3:
                    date = (delimited_response[2],delimited_response[0],delimited_response[1])

            # Attempts to split along '-'
            if date is None:
                delimited_response = response.split("-")
                if len(delimited_response) == 3:
                    date = (delimited_response[0],delimited_response[1],delimited_response[2])

            # None of the formats were used correctly
            if date is None:
                print("One of the specified formats must be followed")
                current_state = State.INPUT_STATE
                continue

            # Attempts to convert string to datetime object.
            try:
                year,month,day = date
                year = int(year)

                # Two-digit years are considered short hand for 20xx. Ex:
                # year = 25, which is interpreted as 2025.
                if year < 100:
                    year += 2000

                # Converts each value to an int and attempts to make a datetime object.
                found_date = datetime(year,int(month),int(day))

                # No errors occured, so move to confirmation state
                current_state = State.CONFIRM_STATE

            # Non numeric character(s) was input.
            except TypeError:
                print("All values must be numeric.")
                current_state = State.INPUT_STATE

            # Ensures date is within the range that can be sent to the database
            except ValueError as e:
                print(f"Values are outside of the acceptable range. {e}")
                current_state = State.INPUT_STATE
    
    # Returns the datetime object, as-is
    if return_datetime:
        return found_date

    # Formats the datetime object into a string that can be used in mysql.
    else:
        return found_date.strftime(return_str_format)


def SelectEntry(entries):
    """Prompts the user to select an entry from a list, looping until they enter a number from within the list. Entries are displayed as 'index+1: {entry}'

    Args:
        entries (): The list of options to choose from.

    Returns: The index for the element in entries that was chosen.
        
    """

    # Prints every entry and an id prepended.
    for i in range(len(entries)):
        if len(entries) > 1:
            print(f"{i+1}: {entries[i]}")
        else:
            print(f"{entries[i]}")
    entry_id = 0
    if len(entries) > 1: # There is more than 1 option, so get choice from user.

        # Continually prompts user for input until something valid is entered.
        while True:
            try:
                entry_id = int(input("Enter number for entry to select it: "))

            # Some none numeric characters were entered
            except ValueError:
                print("Must be numeric.")
                continue

            # Numeric value is outside of the valid range.
            if entry_id <= 0 or entry_id > len(entries):
                print("Value out of range")
                continue

            # Input was valid, so convert to index.
            else:
                entry_id -= 1
                break
    return entry_id
