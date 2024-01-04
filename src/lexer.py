from tokens import *

# Lexer class of luseed
class Lexer(object):
    """
    The Lexer of luseed programming language.
    """
    def __init__(self, source_code: str, file_path: str):
        self.source_code = source_code
        self.file_path = file_path

        # Used to tell the program that the next values are char/strings if this persist at the end of the runtime of the lexer
        # it will return an error for the char/string is not terminated
        self.isChar = False
        self.isString = False

        # Used to tell the program that the next values are for escape sequences
        self.isEscape = False

        # Enables the comment functionality
        self.singleComment = False
        self.multiComment = False

        # Keeps count of the lines for error handling
        self.line_count = 0

        # Keeps count of the character count
        self.char_count = 0

        # Variable that holds the line that started the multi-line comment
        self.line_comment = 0

        # Variable that holds the line where the char started
        self.char_start = 0

        # Variable that holds the line where the string started
        self.string_start = 0

        # Lexeme list refers to the lexemes found in the file
        self.lexeme_list = []
        
        # Token list refers to the list of tokens found in the file
        self.token_list = []

        self.parse()
        
    def parse(self):
        """
        Parses each character in the .lsed file.
        """
        __lexeme = ""
        __oplexeme = ""
        self.line_count = 1

        for char in self.source_code:
            # Checks if char is an alphanumeric character
            if char.isalnum():
                self.char_count += 1
                # Checks if escape sequence is being formulated
                if self.isEscape and self.isString:
                    __oplexeme += char
                    self.isEscape = False
                    # Checks if value in __oplexeme is a valid Escape Sequence
                    if __oplexeme not in ESCAPE_SEQUENCES:
                        print(f"\033[91mERROR: Invalid Escape Sequence at character {self.char_count}, line {self.line_count}.\033[0m")

                    __lexeme += __oplexeme
                    __oplexeme = ""

                else:
                    # Checks if the next inputs are not comments
                    if not self.singleComment and not self.multiComment:

                        __lexeme += char

                    # Appends the current value of the __oplexeme if it is not empty 
                    if __oplexeme != "" and __lexeme != "":
                        self.tokenize(__oplexeme)
                        __oplexeme = ""

            # Checks if char is a special character
            elif char in SPECIAL_CHAR:
                self.char_count += 1
                # Checks if char is in DOUBLE OP for Operators and Comments 
                if char in DOUBLE_OP and not self.isString:
                    if not self.singleComment and not self.multiComment:
                        __oplexeme += char

                    elif self.multiComment:
                        if len(__oplexeme) == 2:
                            if __oplexeme != "*/":
                                __oplexeme = __oplexeme[1:]

                        if char == "*" or char == "/":
                            __oplexeme += char
                
                    # Activates comment boolean if __oplexeme is in comments
                    if __oplexeme in COMMENTS:
                        if __oplexeme == "//":
                            self.singleComment = True

                        elif __oplexeme == "/*":
                            self.multiComment = True
                            self.line_comment = self.line_count

                        elif __oplexeme == "*/" and self.multiComment:
                            self.multiComment = False
                            self.line_comment = 0

                        __oplexeme = ""

                    # Tokenizes the lexemes present in the __lexeme
                    if __lexeme != "":
                        self.tokenize(__lexeme)
                        __lexeme = ""
                
                elif not self.singleComment and not self.multiComment:
                    # Checks if character is double quote for strings
                    if char == "\"":
                        self.string_start = self.line_count
                        __lexeme += char

                        if self.isString:
                            self.isString = False
                            SPECIAL_CHAR.remove(" ")
                            self.tokenize(__lexeme)
                            __lexeme = ""
                        
                        # Appends " " for strings
                        elif not self.isString:
                            self.isString = True
                            SPECIAL_CHAR.append(" ")

                    # Adds the char to __lexeme if isString is active 
                    elif self.isString:
                        # Checks if character is a backslash
                        if self.isEscape or char == "\\":
                            __oplexeme += char
                            if self.isEscape:
                                self.isEscape = False
                                
                                if __oplexeme not in ESCAPE_SEQUENCES:
                                    print(f"\033[91mERROR: Invalid Escape Sequence at character {self.char_count}, line {self.line_count}.\033[0m")
                                
                                __lexeme += __oplexeme
                                __oplexeme = ""
                                    
                            else:
                                self.isEscape = True
                                
                        else:
                            __lexeme += char
                    
                    # Checks if char is a single quotation
                    elif char == "\'":
                        self.char_start = self.line_count
                        __lexeme += char

                        if not self.isChar:
                            self.isChar = True
                        else:
                            self.isChar = False
                            self.char_len = 0

                    # Checks if char is a  period 
                    elif char == ".":
                        if __lexeme.isnumeric():
                            __lexeme += char

                        elif __lexeme.replace("_", "").isalnum() and __lexeme != "":
                            self.tokenize(__lexeme)
                            self.tokenize(char) 
                            __lexeme = ""                      

                    # Checks if char is an underscore or space (For strings)
                    elif char == "_" or char == " ":
                        __lexeme += char

                    else:
                        # Parses the string that was formulated
                        if __lexeme != "" and __lexeme != "\"":
                            self.tokenize(__lexeme)
                            __lexeme = ""

                        # Parses the operator present in __oplexeme
                        if __oplexeme != "":
                            self.tokenize(__oplexeme)
                            __oplexeme = ""

                        # Sets the current char to __lexeme and turns it into a lexeme
                        if char != "\"":
                            self.tokenize(char)

            else:
                # Resets essential values when met with newline "\n"
                if char == "\n":
                    self.singleComment = False
                    self.line_count += 1
                    self.char_count = 0

                if not self.isChar and not self.isString:
                    # tokenizes remaining lexemes
                    if __lexeme != "":
                        self.tokenize(__lexeme)
                        __lexeme = ""
                
        if self.multiComment:
            print(f"\033[91mERROR: MultiLine Comment not concluded in line", self.line_comment, "\033[0m")
        
        if self.isChar:
            print(f"\033[91mERROR: Char literal is not terminated", self.char_start, "\033[0m")

        if self.isString:
            print(f"\033[91mERROR: String literal is not terminated", self.string_start, "\033[0m")

        self.displaytokens()

    def tokenize(self, lexeme: str):
        """
        Determines the token of each lexeme.
        """
        if lexeme in KEYWORDS:
            self.token_list.append([lexeme, KEYWORDS[lexeme]])

        elif lexeme in OP_ASSIGNMENT:
            self.token_list.append([lexeme, OP_ASSIGNMENT[lexeme]])

        elif lexeme in OP_ARITHMETIC:
            self.token_list.append([lexeme, OP_ARITHMETIC[lexeme]])

        elif lexeme in OP_UNARY:
            self.token_list.append([lexeme, OP_UNARY[lexeme]])

        elif lexeme in OP_LOGIC:
            self.token_list.append([lexeme, OP_LOGIC[lexeme]])

        elif lexeme in OP_RELATION:
            self.token_list.append([lexeme, OP_RELATION[lexeme]])

        elif lexeme in DELIMITERS:
            self.token_list.append([lexeme, DELIMITERS[lexeme]])

        elif lexeme in ESCAPE_SEQUENCES:
            self.token_list.append([lexeme, ESCAPE_SEQUENCES[lexeme]])

        elif lexeme.isnumeric():
            self.token_list.append([lexeme, "INT_LITERAL"])

        elif len(lexeme) > 1 and (lexeme[-1] == "f") and (lexeme[-2] != ".") and self.isfloat(lexeme.replace("f", "")):
            self.token_list.append([lexeme, "FLOAT_LITERAL"])

        elif len(lexeme) > 1 and ("." in lexeme) and (lexeme[-1] != ".") and self.isfloat(lexeme):
            self.token_list.append([lexeme, "DOUBLE_LITERAL"])

        elif lexeme[0] == "\"" and lexeme[-1] == "\"":
            self.token_list.append([lexeme, "STRING_LITERAL"])

        elif lexeme[0] == "\'" and lexeme[-1] == "\'":
            if len(lexeme.replace("\'", "")) == 1: 
                self.token_list.append([lexeme, "CHAR_LITERAL"])
            else:
                print(f"\033[91mERROR: Invalid Character Literal at character {self.char_count}, line {self.line_count}.\033[0m")
                self.token_list.append([lexeme, "INVALID_CHAR_LITERAL"])
        else:
            if len(lexeme) > 0 and lexeme[0].isalpha() and lexeme.replace("_", "").isalnum():
                self.token_list.append([lexeme, "IDENTIFIER"])
            else:
                print(f"\033[91mERROR: Unknown Token in line {self.line_count}.\033[0m")
                self.token_list.append([lexeme, "UNKNOWN_TOKEN"])

    def isfloat(self, value):
        """
        Tests a value if it is a valid float
        """
        try:
            float(value)
            return True
        
        except ValueError:
            return False

    def displaytokens(self):
        """
        Displays the tokens found in the file.
        """

        print()
        for token in self.token_list:
            print(token)

    def returntokens(self):
        """
        Returns the tokens found in the file.
        """
        return self.token_list