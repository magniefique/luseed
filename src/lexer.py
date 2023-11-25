from tokens import *

# Lexer class of luseed
class Lexer(object):
    """
    The Lexer of luseed programming language.
    """
    def __init__(self, source_code: str):
        self.source_code = source_code
        
        self.isChar = False
        self.isString = False
        self.isProperty = False
        self.singleComment = False
        self.multiComment = False

        self.line_count = 1
        self.line_comment = None

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
                if not self.singleComment and not self.multiComment:
                    __lexeme += char

                # Appends the current value of the __oplexeme if it is not empty 
                if __oplexeme != "" and __lexeme != "":
                    self.tokenize(__oplexeme)
                    __oplexeme = ""

            # Checks if char is a special character
            elif char in SPECIAL_CHAR:
                
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
                            self.line_comment = None

                        __oplexeme = ""

                    # Tokenizes the lexemes present in the __lexeme
                    if __lexeme != "":
                        self.tokenize(__lexeme)
                        __lexeme = ""
                
                elif not self.singleComment and not self.multiComment:
                    # Checks if character is double quote for strings
                    if char == "\"":
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
                        __lexeme += char
                    
                    # Checks if char is a single quotation
                    elif char == "\'":
                        if not self.isChar:
                            self.isChar = True
                        else:
                            self.isChar = False

                    # Checks if char is a  period 
                    elif char == ".":
                        if __lexeme.isnumeric():
                            __lexeme += char

                        elif __lexeme.replace("_", "").isalnum() and __lexeme != "":
                            self.tokenize(__lexeme)
                            self.tokenize(char) 
                            __lexeme = ""
                            self.isProperty = True                         

                    # Checks if char is single quote for char literals and spaces for string values
                    elif char == "_" or char == " ":
                        __lexeme += char

                    else:
                        # Parses the string that was formulated
                        if __lexeme != "" and __lexeme != "\"":
                            self.tokenize(__lexeme)
                            __lexeme = ""

                            if self.isProperty:
                                self.isProperty = False

                        # Parses the operator present in __oplexeme
                        if __oplexeme != "":
                            self.tokenize(__oplexeme)
                            __oplexeme = ""

                        # Sets the current char to __lexeme and turns it into a lexeme
                        if char != "\"":
                            self.tokenize(char)

            else:
                if char == "\n":
                    self.singleComment = False
                    self.line_count += 1

                # Makes the string a lexeme if char is " " and not in SPECIAL CHARACTERS
                if __lexeme != "":
                    self.tokenize(__lexeme)
                    __lexeme = ""
                
        if self.multiComment:
            print(f"\033[91mERROR: MultiLine Comment not concluded in line", self.line_comment, "\033[0m")
            #exit(1)
        
        if self.isChar:
            print(f"\033[91mERROR: Char literal is not terminated", self.line_comment, "\033[0m")

        if self.isString:
            print(f"\033[91mERROR: String literal is not terminated", self.line_comment, "\033[0m")

        

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

        elif lexeme.isnumeric() and not self.isProperty:
            self.token_list.append([lexeme, "int_literal"])

        elif lexeme[-1] == "f" and self.isfloat(lexeme.replace("f", "")):
            self.token_list.append([lexeme, "float_literal"])

        elif self.isfloat(lexeme) and "." in lexeme:
            self.token_list.append([lexeme, "double_literal"])

        elif "\"" in lexeme:
            self.token_list.append([lexeme, "string_literal"])

        elif "\'" in lexeme:
            self.token_list.append([lexeme, "char_literal"])

        else:
            if len(lexeme) > 0 and lexeme[0].isalpha() and lexeme.replace("_", "").isalnum():
                self.token_list.append([lexeme, "identifier"])
            else:
                print(f"\033[91mERROR: Unknown Token in line", self.line_count, "\033[0m")
                #exit(1)
                self.token_list.append([lexeme, "unknown"])

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
        for token in self.token_list:
            print(token)

    def returntokens(self):
        """
        Returns the tokens found in the file.
        """
        return self.token_list