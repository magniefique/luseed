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

        self.lexemize()
        self.tokenize()
        self.displaytokens()

    # Separates each character and formulates each lexeme
    def lexemize(self):
        __lexeme = ""
        for char in self.source_code:
            if char.isalnum():
                __lexeme += char    
            elif char in SPECIAL_CHAR:
                # Checks if char is a whitespace
                if char == " ":
                    __lexeme += char
                    continue

                if self.isString:
                    __lexeme += "\""

                # Checks if current special character is a quotation
                if (char == "\"" or char == "\'") and self.isString == False:
                    self.isString = True
                    SPECIAL_CHAR.append(" ")

                elif (char == "\"" or char == "\'") and self.isString == True:
                    self.isString = False
                    SPECIAL_CHAR.remove(" ")

                # Leximizes the string that was formulated
                if __lexeme != "" and __lexeme != "\"":
                    self.lexeme_list.append(__lexeme)
                    __lexeme = ""

                # Sets the current char to __lexeme and turns it into a lexeme
                if char != "\"":
                    __lexeme += char
                    self.lexeme_list.append(__lexeme)
                    __lexeme = ""

    # Function that determines the tokens of each lexeme
    def tokenize(self):
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
            elif regex.match("[a-z]", lexeme) or regex.match("[A-Z]", lexeme):
                if regex.match(".*?", lexeme):
                    self.token_list.append(["\"" + lexeme, "string_literal"])
                else:
                    self.token_list.append([lexeme, "identifier"])
            elif lexeme.isnumeric():
                self.token_list.append([lexeme, "int_literal"])

    # Function that displays the tokens
    def displaytokens(self):
        for token in self.token_list:
            print(token)