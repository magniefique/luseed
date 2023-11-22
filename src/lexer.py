from tokens import *
import regex

# Lexer class of luseed
class Lexer(object):
    """
    The Lexer of luseed programming language.
    """
    def __init__(self, source_code: str):
        self.source_code = source_code
        
        self.isString = False

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
        __line_count = 1

        for char in self.source_code:
            
            # Checks if char is an alphanumeric character
            if char.isalnum():
                __lexeme += char

                # Appends the current value of the __oplexeme if it is not empty 
                if __oplexeme != "" and __lexeme != "":
                    self.lexeme_list.append(__oplexeme)
                    self.tokenize(__oplexeme)
                    __oplexeme = ""
            
            # Checks if char is a special character
            elif char in SPECIAL_CHAR:
                
                # Checks if character is double quote for strings
                if char == "\"":
                    __lexeme += char

                    if self.isString:
                        self.isString = False
                        SPECIAL_CHAR.remove(" ")
                        self.lexeme_list.append(__lexeme)
                        self.tokenize(__lexeme)
                        __lexeme = ""
                    
                    # Appends " " for strings
                    elif not self.isString:
                        self.isString = True
                        SPECIAL_CHAR.append(" ")

                # Checks if char is single quote for char literals and spaces for string values
                elif char == "\'" or char == "_" or char == " ":
                    __lexeme += char

                # Checks if char is in DOUBLE OP for Operators such as logical and assignment
                elif char in DOUBLE_OP and not self.isString:
                    __oplexeme += char

                # Checks if char is a period and 
                elif char == "." and not self.isString:
                    if __lexeme.isnumeric():
                        __lexeme += char

                # Adds the char to __lexeme if isString is active 
                elif self.isString:
                    __lexeme += char

                else:
                    # Parses the string that was formulated
                    if __lexeme != "" and __lexeme != "\"":
                        self.lexeme_list.append(__lexeme)
                        self.tokenize(__lexeme)
                        __lexeme = ""
                    
                    if __lexeme != "":
                        __lexeme += char
                        self.lexeme_list.append(__lexeme)
                        self.tokenize(__lexeme)
                        __lexeme = ""

                    # Parses the operator present in __oplexeme
                    if __oplexeme != "":
                        self.lexeme_list.append(__oplexeme)
                        self.tokenize(__oplexeme)
                        __oplexeme = ""

                    # Sets the current char to __lexeme and turns it into a lexeme
                    if char != "\"":
                        __lexeme += char
                        self.lexeme_list.append(__lexeme)
                        self.tokenize(__lexeme)
                        __lexeme = ""

            else:
                # Makes the string a lexeme if char is " " and not in SPECIAL CHARACTERS
                if __lexeme != "":
                    self.lexeme_list.append(__lexeme)
                    self.tokenize(__lexeme)
                    __lexeme = ""
        
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
            self.token_list.append([lexeme, "int_literal"])

        elif self.isfloat(lexeme):
            self.token_list.append([lexeme, "float_literal"])

        elif "\"" in lexeme:
            self.token_list.append([lexeme, "string_literal"])

        elif "\'" in lexeme:
            self.token_list.append([lexeme, "char_literal"])

        else:
            if len(lexeme) > 0 and lexeme.replace("_", "").isalnum():
                self.token_list.append([lexeme, "identifier"])
            else: 
                self.token_list.append([lexeme, "unknown"])

    def isfloat(self, value: str):
        """
        Checks if the passed value is a float.
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