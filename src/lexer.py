from tokens import *
import regex

# Lexer class of luseed
class Lexer(object):

    def __init__(self, source_code):
        self.source_code = source_code
        self.isString = False
        # Lexeme list refers to the lexemes found in the file
        self.lexeme_list = []
        
        # Token list refers to the list of tokens found in the file
        self.token_list = []

        self.parse()
        self.tokenize()

    # Separates each character and formulates each lexeme
    def parse(self):
        __lexeme = ""
        __oplexeme = ""
        for char in self.source_code:
            if char.isalnum():
                __lexeme += char

                # Appends the current value of the __oplexeme as a lexeme if the char is not alpha and adds to the lexeme if alpha
                if __oplexeme != "":
                    if not char.isalpha():
                        self.lexeme_list.append(__oplexeme)
                        __oplexeme = ""
                   
                    else:
                        __lexeme += __oplexeme
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
                        __lexeme = ""
                    
                    # Appends " " for strings
                    elif not self.isString:
                        self.isString = True
                        SPECIAL_CHAR.append(" ")

                # Checks if char is single quote for char literals and spaces for string values
                elif char == "\'" or char == " " or char == "_":
                    __lexeme += char

                elif char == "." and not self.isString:
                    if __lexeme.isnumeric():
                        __lexeme += char

                # Checks if char is in DOUBLE OP for Operators such as logical and assignment
                elif char in DOUBLE_OP and not self.isString:
                    __oplexeme += char

                # Adds the char to __lexeme if isString is active 
                elif self.isString:
                    __lexeme += char

                else:
                    # Parses the string that was formulated
                    if __lexeme != "" and __lexeme != "\"":
                        self.lexeme_list.append(__lexeme)
                        __lexeme = ""

                    if __lexeme != "":
                        __lexeme += char
                        self.lexeme_list.append(__lexeme)
                        __lexeme = ""

                    # Parses the operator present in __oplexeme
                    if __oplexeme != "":
                        self.lexeme_list.append(__oplexeme)
                        __oplexeme = ""

                    # Sets the current char to __lexeme and turns it into a lexeme
                    if char != "\"":
                        __lexeme += char
                        self.lexeme_list.append(__lexeme)
                        __lexeme = ""

            else:
                # Makes the string a lexeme if char is " " and not in SPECIAL CHARACTERS
                if __lexeme != "":
                    self.lexeme_list.append(__lexeme)
                    __lexeme = ""

    # Function that determines the tokens of each lexeme
    def tokenize(self):
        __linecount = 1
        for lexeme in self.lexeme_list:
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
                    print(f"\033[91mERROR: Unknown Token in Line ", __linecount, "\033[0m")
                    self.token_list.append([lexeme, "unknown"])
            
            if lexeme[0] == ";":
                __linecount += 1

        self.displaytokens()

    # Checks if the lexeme is a float
    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Function that displays the tokens
    def displaytokens(self):
        for token in self.token_list:
            print(token)

    # Returns tokens
    def returntokens(self):
        return self.token_list