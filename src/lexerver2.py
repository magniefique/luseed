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

        # Keeps count for the length of char 
        self.char_len = 0

        # Used to tell the program that the next values are for escape sequences
        self.isEscape = False

        # Enables the comment functionality
        self.singleComment = False
        self.multiComment = False

        # Keeps count of the lines for error handling
        self.line_count = 0

        # Keeps count of the character count
        self.char_count = 0

        # Stores the line and character where the char started
        self.char_line = 0
        self.char_start = 0

        # Stores the line and character where the string started
        self.string_line = 0
        self.string_start = 0

        # Variable that holds the line that started the multi-line comment
        self.line_comment = 0

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

        # Loop that takes care of the formulation of lexemes
        for char in self.source_code:
            # Checks if the current character is a new line character
            if char == "\n":
                self.singleComment = False
                self.line_count += 1
                self.char_count = 0

            # Checks if the current character is an empty space and tokenize current lexemes
            if char == " " and not self.isString and not self.isChar:
                # tokenizes remaining lexemes
                if __lexeme != "":
                    self.tokenize(__lexeme)
                    __lexeme = ""

            # Checks if the following character/s is not a part of a comment
            if not self.singleComment and not self.multiComment:
                self.char_count += 1
                
                # Checks if the next character/s is not a part of a char value or str value
                if not self.isString and not self.isChar:
                    # Checks if char is an alphanumeric value
                    if char.isalnum():
                        __lexeme += char
                    
                        # Appends the current value of the __oplexeme if it is not empty 
                        if __oplexeme != "" and __lexeme != "":
                            self.tokenize(__oplexeme)
                            __oplexeme = ""
                    
                    # Checks if char is an accepted special character
                    elif char in SPECIAL_CHAR:
                        # Checks if char is part of an operator that contains 2 characters
                        if char in DOUBLE_OP:
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

                        # Checks if character is a double quotation for str literals
                        elif char == "\"":
                            self.string_line = self.line_count
                            __lexeme += char
                            self.isString = True

                        # Checks if character is a single quotation for char literals
                        elif char == "\'":
                            self.char_line = self.line_count
                            __lexeme += char
                            self.isChar = True

                        # Checks if char is a period 
                        elif char == ".":
                            # Checks if the contents of the __lexeme is numeric for floating-point values
                            if __lexeme.isnumeric():
                                __lexeme += char

                            # Checks if the current value of the __lexeme is a valid Identifier for property
                            elif __lexeme.replace("_", "").isalnum() and __lexeme != "":
                                self.tokenize(__lexeme)
                                self.tokenize(char) 
                                __lexeme = ""
                        
                        # Append char to __lexeme if it is an underscore
                        elif char == "_":
                            __lexeme += char
                        
                        else:
                            # Parses the string that was formulated
                            if __lexeme != "":
                                self.tokenize(__lexeme)
                                __lexeme = ""

                            # Parses the operator present in __oplexeme
                            if __oplexeme != "":
                                self.tokenize(__oplexeme)
                                __oplexeme = ""

                            # Sets the current char to __lexeme and turns it into a lexeme
                            if char != "\"":
                                self.tokenize(char)

                # Checks if the following character/s is a part of string
                elif self.isString:
                    # Checks if the next char value is used for an Escape Sequence (Ex. "\n")
                    if self.isEscape:
                        # Checks if character is not part of the ESCAPE_CHAR and return an error if true
                        if char not in ESCAPE_CHAR:
                            print(f"\033[91mERROR: Invalid Escape Sequence at character {self.char_count}, line {self.line_count}.\033[0m")

                        __oplexeme += char
                        __lexeme += __oplexeme
                        __oplexeme = ""
                        self.isEscape = False

                    else:
                        # Check if the current char is a double quote to terminate the string
                        if char == "\"":
                            __lexeme += char
                            self.tokenize(__lexeme)
                            __lexeme = ""
                            self.isString = False

                        # Check if the current char is a backslash to create an escape character/sequence
                        elif char == "\\":
                            __oplexeme += char
                            self.isEscape = True
                            
                        else:
                            __lexeme += char
                
                # Checks if the following character is a literal character value
                elif self.isChar:
                    # Check if the current char is a double quote to terminate the char literal
                    if char == "\'":
                        __lexeme += char
                        self.tokenize(__lexeme)
                        self.isChar = False
                        self.char_len = 0
                        __lexeme = ""

                    else:
                        __lexeme += char
                            

            # Checks if the following character/s is a part of a multi-line comment
            elif self.multiComment:
                # Check if the length of the __oplexeme is equal to 2
                if len(__oplexeme) == 2:
                    # If not equal to the terminator for comments, remove the first character of the string __oplexeme
                    if __oplexeme != "*/":
                        __oplexeme = __oplexeme[1:]

                    # If it is, turn off the multi-comment
                    else:
                        self.multiComment = False
                        __oplexeme = ""

                # Checks if character is a substring of the terminator of multiline comments
                if char == "*" or char == "/":
                    __oplexeme += char

        # Checks whether there is an unterminated multi-line comment, character, and string
        if self.multiComment:
            print(f"\033[91mERROR: MultiLine Comment not concluded in line", self.line_comment, "\033[0m")
        
        if self.isChar:
            print(f"\033[91mERROR: Char literal is not terminated", self.char_line, "\033[0m")

        if self.isString:
            print(f"\033[91mERROR: String literal is not terminated", self.string_line, "\033[0m")

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
                print(f"\033[91mERROR: Invalid Character Literal at character {self.char_count} line {self.line_count}.\033[0m")
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
    