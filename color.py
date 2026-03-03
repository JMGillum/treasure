class ColoredText:

    """ Stores text that is colored.

    Attributes: 
        colors: Definitions of colors that are supported.
        enable_color: Toggles color output
        use_8_bit_colors: Toggles using 8 bit colors instead of 3 bit colors.
        toggles: Specific toggles that can toggle colors off
    """

    colors = {
        "blue": (34, 4),
        "bright_yellow": (33, 11),
        "bronze": (31, 202),
        "green": (32, 2),
        "lime": (32, 82),
        "magenta": (35, 163),
        "pink": (31, 213),
        "purple": (35, 5),
        "red": (31, 1),
        "rose": (31, 204),
        "silver": (37, 231),
        "teal": (36, 6),
        "yellow": (33, 3),
    }

    enable_color = True
    use_8_bit_colors = True

    toggles = {}

    def SetToggleCategory(toggle:str, value:bool=True):
        """ Creates a new toggle category or updates an existing one.

        Args:
            toggle: The category to create. Stored as a key in the ColoredText.toggles dict
            value: The value to set the toggle category to.
        """
        
        ColoredText.toggles |= {toggle:value}

    def __init__(self, text:str, color:str, toggle:str=None):
        """ Sets up the text with its color.

        Args:
            text: The text to display
            color: The string corresponding to a key in ColoredText.colors to print the text in.
            toggle: An optional string corresponding to a key in ColoredText.toggles to enable additional checking as to whether to print in color.
        """
        
        self.status = {}
        self.SetText(text)
        self.SetColor(color)
        self.SetToggle(toggle)

    def Status(self)->dict:
        """ Returns the self.status dictionary, which stores whether the text, color, and toggle were valid.

        Returns: self.status
            
        
        """
        return self.status

    def SetText(self, text:str)->bool:
        """ Sets the text attribute

        Args:
            text: Should be castable to str. The text that will be displayed.

        Returns: True on success.
            
        """

        self.text = text
        self.status |= {"text":True}
        return True


    def SetColor(self, color:str)->bool:
        """ Sets which color the text will be displayed in.

        Args:
            color: Should be a string corresponding to a key in ColoredText.colors

        Returns: True on success. False if color is not a valid key in ColoredText.colors.
            
        """

        status = False
        try:
            self.color = color.strip().lower()
            status = True

            # Checks if color is defined
            try:
                ColoredText.colors[self.color]
            except KeyError:
                status = False

        except ValueError, AttributeError:
            self.color = None

        self.status |= {"color":status}
        return status


    def SetToggle(self, toggle:str)->bool:
        """ Sets the toggle attribute

        Args:
            toggle: A string corresponding to a value in ColoredText.toggles. Output will only be colored if the value in this dictionary is True

        Returns: True on success, None if toggle is None, False otherwise.
            
        """

        status = None
        if toggle is not None:
            status = False

            try:
                self.toggle = str(toggle)
                status = True
            except ValueError:
                self.toggle = None

        else:
            self.toggle = None

        self.status |= {"toggle":status}
        return status


    def WillPrintColors(self)->bool:
        """ Checks whether the output should be colored. Checks if color is enabled, and if the optional toggle is enabled and set to True

        Returns: True if output should be colored, False otherwise.
            
        """

        if not ColoredText.enable_color:
            return False

        if self.toggle is not None:
            try:
                return ColoredText.toggles[self.toggle]
            except KeyError:
                return False

        return True


    def Print(self)->str:
        """ Creates a string with ANSI escape sequences that enable color output (if applicable)

        Returns: string of the text with applicable escape sequences. If output is not to be colored, simple returns the text.
            
        """

        # Color output is disabled
        if not self.WillPrintColors():
            return str(self.text)

        index = 1 if ColoredText.use_8_bit_colors else 0

        prefix = ("\033[", "\033[38:5:")
        suffix = ("m", "m")
        default = ("\033[0m", "\033[39;49m")

        color_string = ""
        ansi_string = ""

        # Attempts to retrieve color from dictionary
        try:
            color_string = ColoredText.colors[self.color][index]

        # Color is not defined, so return text unchanged
        except KeyError:
            return str(self.text)

        # Entire ansi sequence for colored text
        ansi_string = f"{prefix[index]}{color_string}{suffix[index]}"

        return f"{ansi_string}{self.text}{default[index]}"


    def __str__(self):
        return self.Print()


    def __len__(self):
        return len(self.text)


    def __gt__(self,other):
        return self.text > other.text


    def __lt__(self,other):
        return self.text < other.text


    def __eq__(self,other):
        return self.text == other.text


    def __le__(self,other):
        return self.text <= other.text


    def __ge__(self,other):
        return self.text >= other.text


    def __ne__(self,other):
        return self.text != other.text

