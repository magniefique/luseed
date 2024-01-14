from luseed_tokens import *
from luseed_token import *
from fpdf import FPDF
import time

# Lexer class of luseed
class Lexer(object):
    """
    The Lexer of luseed programming language.
    """
    def __init__(self, source_code: str, file_path: str):
        self.source_code: str = source_code
        self.file_path: str = file_path

        # Used to store values for lexemes and operational lexemes
        self.lexeme = ''
        self.oplexeme = ''

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

        # Stores the line and character where the char started
        self.char_line = 0
        self.char_start = 0

        # Stores the line and character where the string started
        self.string_line = 0
        self.string_start = 0

        # Variable that holds the line that started the multi-line comment
        self.comment_line = 0
        self.comment_start = 0
        
        # Token list refers to the list of tokenized lexemes found in the file
        self.tokenized_lexemes = []

        # Parses the code
        start = time.time()
        self.parsecode()
        end = time.time()

        # Computes for the Elapsed Time
        self.elapsed_time = str(end - start)

        # Generates file for the Symbol Table
        self.generatefile()

        # Returns tokens
        self.returntokens()

    def parsecode(self):
        """
        Parses each character in the .lsed code.
        """
        self.line_count = 1

        for char in self.source_code:
            self.char_count += 1

            # Checks for whitespace characters
            if char in WHITESPACES:
                self.parsewhite(char)
            
            # Checks if next character/s are not part of a comment
            if not self.singleComment and not self.multiComment:
                # Checks if next character/s are not part of a String literal or Char literal
                if not self.isString and not self.isChar:
                    if char.isalnum():
                        self.parsealnum(char)

                    elif char in SPECIAL_CHAR:
                        self.parsespec(char)
                
                # Checks if next character is part of a Char literal
                elif self.isChar:
                    self.parsechar(char)

                # Checks if next character/s are not part of a String literal
                elif self.isString:
                    self.parsestring(char)

            # Checks if the following character/s is a part of a single-line comment
            elif self.singleComment:
                self.parsecomment(char, "single")

            # Checks if the following character/s is a part of a multi-line comment
            elif self.multiComment:
                self.parsecomment(char, "multi")
                
    def parsealnum(self, char: str):
        """
        Responsible for parsing alphanumeric characters.
        """
        self.lexeme += char
                    
        # Appends the current value of the self.oplexeme if it is not empty 
        if self.oplexeme != "" and self.lexeme != "":
            self.tokenize(self.oplexeme)
            self.oplexeme = ""

    def parsespec(self, char: str):
        """
        Responsible for parsing special characters
        """
        # Checks if char is part of an operator that contains 2 characters
        if char in DOUBLE_OP:
            self.oplexeme += char

            # Activates comment boolean if self.oplexeme is in comments
            if self.oplexeme in COMMENTS:
                if self.oplexeme == "//":
                    self.singleComment = True

                elif self.oplexeme == "/*":
                    self.multiComment = True
                    self.comment_line = self.line_count
                    self.comment_start = self.char_count

                self.tokenize(self.oplexeme)
                self.oplexeme = ""
            
            # Tokenizes the lexemes present in the self.lexeme
            if self.lexeme != "":
                self.tokenize(self.lexeme)
                self.lexeme = ""
                
        else:
            # Appends the current value of the self.oplexeme if it is not empty 
            if self.oplexeme != "":
                self.tokenize(self.oplexeme)
                self.oplexeme = ""

            # Checks if character is a double quotation for str literals
            if char == "\"":
                self.string_line = self.line_count
                self.lexeme += char
                self.isString = True

            # Checks if character is a single quotation for char literals
            elif char == "\'":
                self.char_line = self.line_count
                self.lexeme += char
                self.isChar = True

            # Checks if char is a period 
            elif char == ".":
                # Checks if the contents of the self.lexeme is numeric for floating-point values
                if self.lexeme.isnumeric():
                    self.lexeme += char

                # Checks if the current value of the self.lexeme is a valid Identifier for property
                elif self.lexeme.replace("_", "").isalnum() and self.lexeme != "":
                    self.tokenize(self.lexeme)
                    self.tokenize(char) 
                    self.lexeme = ""
            
            # Append char to self.lexeme if it is an underscore
            elif char == "_":
                self.lexeme += char
            
            else:
                # Parses the string that was formulated
                if self.lexeme != "":
                    self.tokenize(self.lexeme)
                    self.lexeme = ""

                # Parses the operator present in self.oplexeme
                if self.oplexeme != "":
                    self.tokenize(self.oplexeme)
                    self.oplexeme = ""

                # Sets the current char to self.lexeme and turns it into a lexeme
                self.tokenize(char)

    def parsewhite(self, char: str):
        """
        Responsible for parsing whitespaces
        """
        # Checks if the current character is a new line character
        if char == "\n":
            self.singleComment = False

            # Resets both Char and String when new line is introduced
            if self.isChar:
                self.tokenize(self.lexeme)
                self.isChar = False
                self.lexeme = ""
            
            if self.isString:
                self.tokenize(self.lexeme)
                self.isString = False
                self.lexeme = ""

            self.line_count += 1
            self.char_count = 0
        
        elif char == " " and not self.isString:
            if self.lexeme != "":
                self.tokenize(self.lexeme)
                self.lexeme = ""
            
            if self.oplexeme != "":
                self.tokenize(self.oplexeme)
                self.oplexeme = ""

    def parsechar(self, char: str):
        """
        Handles character literal values.
        """
        # Check if the current char is a double quote to terminate the char literal
        if char == "\'":
            self.lexeme += char
            self.tokenize(self.lexeme)
            self.isChar = False
            self.lexeme = ""

        else:
            self.lexeme += char
    
    def parsestring(self, char: str):
        """
        Handles string literal values.
        """
        # Checks if the next char value is used for an Escape Sequence (Ex. "\n")
        if self.isEscape:
            # Checks if character is not part of the ESCAPE_CHAR and return an error if true
            if char not in ESCAPE_CHAR:
                print(f"\033[91mERROR: Invalid Escape Sequence at character {self.char_count}, line {self.line_count}.\033[0m")

            self.oplexeme += char
            self.lexeme += self.oplexeme
            self.oplexeme = ""
            self.isEscape = False

        else:
            # Check if the current char is a double quote to terminate the string
            if char == "\"":
                self.lexeme += char
                self.tokenize(self.lexeme)
                self.lexeme = ""
                self.isString = False

            # Check if the current char is a backslash to create an escape character/sequence
            elif char == "\\":
                self.oplexeme += char
                self.isEscape = True
            
            else:
                self.lexeme += char

    def parsecomment(self, char: str, type: str):
        if type == "single":
            pass

        elif type == "multi":
            # Check if the length of the self.oplexeme is equal to 2
            if len(self.oplexeme) == 2:
                # If not equal to the terminator for comments, remove the first character of the string self.oplexeme
                if self.oplexeme != "*/":
                    self.oplexeme = self.oplexeme[1:]

                # If it is, turn off the multi-comment
                else:
                    self.multiComment = False
                    self.comment_line = 0
                    self.comment_start = 0
                    self.oplexeme = ""

            # Checks if character is a substring of the terminator of multiline comments
            if char == "*" or char == "/":
                self.oplexeme += char

    def tokenize(self, lexeme: str):
        """
        Determines the token of each lexeme.
        """
        if lexeme in KEYWORDS:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, KEYWORDS[lexeme]))
        
        elif lexeme in NOISEWORDS:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, NOISEWORDS[lexeme]))

        elif lexeme in OP_ASSIGNMENT:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, OP_ASSIGNMENT[lexeme]))

        elif lexeme in OP_ARITHMETIC:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, OP_ARITHMETIC[lexeme]))

        elif lexeme in OP_UNARY:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, OP_UNARY[lexeme]))

        elif lexeme in OP_RELATION:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, OP_RELATION[lexeme]))

        elif lexeme in DELIMITERS:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, DELIMITERS[lexeme]))

        elif lexeme in ESCAPE_SEQUENCES:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, ESCAPE_SEQUENCES[lexeme]))

        elif lexeme in COMMENTS:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, COMMENTS[lexeme]))
        
        elif lexeme.isnumeric():
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, 'INT_LITERAL'))

        elif len(lexeme) > 1 and (lexeme[-1] == "f") and (lexeme[-2] != ".") and self.isfloat(lexeme.replace("f", "")):
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, 'FLOAT_LITERAL'))

        elif len(lexeme) > 1 and ("." in lexeme) and (lexeme[-1] != ".") and self.isfloat(lexeme):
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, 'DOUBLE_LITERAL'))

        elif lexeme[0] == "\"" and lexeme[-1] == "\"":
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, 'STRING_LITERAL'))

        elif lexeme[0] == "\'" and lexeme[-1] == "\'":
            if len(lexeme.replace("\'", "")) == 1:
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, 'CHAR_LITERAL'))
            else:
                print(f"\033[91mERROR: Invalid Character Literal at character {self.char_count-1} line {self.line_count}.\033[0m")
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, 'UNKNOWN_TOKEN'))

        else:
            if len(lexeme) > 0 and lexeme[0].isalpha() and lexeme.replace("_", "").isalnum():
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, 'IDENTIFIER'))
            else:
                print(f"\033[91mERROR: Unknown Token at character {self.char_count-1}, line {self.line_count}.\033[0m")
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, 'UNKNOWN_TOKEN'))

    def isfloat(self, value):
        """
        Tests a value if it is a valid float
        """
        try:
            float(value)
            return True
        
        except ValueError:
            return False

    def display_console(self):
        """
        Displays the Symbol Table in the Terminal
        """
        longest_1 = 0
        longest_2 = 0

        display_list = [["LINE", "LEXEME", "TOKEN"]]
        display_list.extend(self.tokenized_lexemes)

        print(f"\n\033[1mSYMBOL TABLE for {self.file_path}\033[0m")
        print(f"Total Tokenized Lexemes:\t{len(self.tokenized_lexemes)}\n")

        # Calculates length of space
        for i in range(len(display_list)):
            if i == 0:
                length_1 = len(display_list[i][0])
                length_2 = len(display_list[i][1])

            else:
                length_1 = len(display_list[i].line)
                length_2 = len(display_list[i].lexeme)

            if (length_1 > longest_1):
                longest_1 = length_1
            
            if (length_2 > longest_2):
                longest_2 = length_2

        # Displays the symbol table in the console
        for i in range(len(display_list)):
            if i == 0:
                spacing_1 = ((longest_1 - len(display_list[i][0])) + 4) * " "
                spacing_2 = ((longest_2 - len(display_list[i][1])) + 20) * " "
                print(f"\033[1m{display_list[i][0]}\033[0m{spacing_1}|\033[1m{display_list[i][1]}\033[0m{spacing_2}|\033[1m{display_list[i][2]}\033[0m")

            else:
                spacing_1 = ((longest_1 - len(display_list[i].line)) + 4) * " "
                spacing_2 = ((longest_2 - len(display_list[i].lexeme)) + 20) * " "
                print(f"{display_list[i].line}{spacing_1}|{display_list[i].lexeme}{spacing_2}|{display_list[i].token}")

    def generatefile(self):
        """
        Generates the symbol table of the source code
        """
        PDF_TABLE = [["LINE", "LEXEME", "TOKEN"]]
        PDF_TABLE.extend(self.tokenized_lexemes)

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Inconsolata", "",
                     fname="C:\\Users\\xcharuzu\\Documents\\GitHub\\luseed\\font\\Inconsolata-Regular.ttf",
                     uni=True)
        
        pdf.add_font("Inconsolata", "B",
                     fname="C:\\Users\\xcharuzu\\Documents\\GitHub\\luseed\\font\\Inconsolata-Bold.ttf",
                     uni=True)
        
        pdf.set_font("Inconsolata", "B", size=16)
        pdf.cell(txt="SYMBOL TABLE for " + self.file_path, ln=1, center=True)
        pdf.set_font("Inconsolata", "", size=12)
        pdf.cell(txt=" ", ln=1)
        pdf.cell(txt="Total Tokenized Lexemes: " + str(len(self.tokenized_lexemes)), ln=1)
        pdf.cell(txt="Elapsed Time:            " + self.elapsed_time, ln=1)
        pdf.cell(txt=" ", ln=1)
        with pdf.table(col_widths=(15, 40, 40)) as table:
            for i in range(len(PDF_TABLE)):
                row = table.row()
                tkn_array = PDF_TABLE[i] if i == 0 else [PDF_TABLE[i].line, PDF_TABLE[i].lexeme, PDF_TABLE[i].token]
                
                for datum in tkn_array:
                    row.cell(datum)
                
        pdf.output(name='src/symboltable/SYMBOL_TABLE_' + self.file_path + ".pdf", dest="F")

    def returntokens(self):
        """
        Returns the tokens found in the file.
        """
        return self.tokenized_lexemes