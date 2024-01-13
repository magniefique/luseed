from tokens import *
from fpdf import FPDF
import time

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
        self.tokenized_list = []

        # Parses the code
        start = time.time()
        self.parse()
        end = time.time()

        # Computes for the Elapsed Time
        self.elapsed_time = str(end - start)

        # Generates file for the Symbol Table
        self.generatefile()

        # Returns tokens
        self.returntokens()

    def parse(self):
        """
        Parses each character in the .lsed file.
        """
        __lexeme = ""
        __oplexeme = ""
        self.line_count = 1

        # Loop that takes care of the formulation of lexemes
        for char in self.source_code:
            self.char_count += 1
            # Checks if the current character is a new line character
            if char == "\n":
                self.singleComment = False

                # Resets both Char and String when new line is introduced
                if self.isChar:
                    self.tokenize(__lexeme)
                    self.isChar = False
                    __lexeme = ""
                
                if self.isString:
                    self.tokenize(__lexeme)
                    self.isString = False
                    __lexeme = ""

                self.line_count += 1
                self.char_count = 0

            # Checks if the following character/s is not a part of a comment
            if not self.singleComment and not self.multiComment:
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
                                    self.comment_line = self.line_count
                                    self.comment_start = self.char_count

                                self.tokenize(__oplexeme)
                                __oplexeme = ""
                            
                            # Tokenizes the lexemes present in the __lexeme
                            if __lexeme != "":
                                self.tokenize(__lexeme)
                                __lexeme = ""
                        else:
                            # Appends the current value of the __oplexeme if it is not empty 
                            if __oplexeme != "":
                                self.tokenize(__oplexeme)
                                __oplexeme = ""

                            # Checks if character is a double quotation for str literals
                            if char == "\"":
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

                    # Checks if the current character is an empty space and tokenize current lexemes
                    if char == " ":
                        # tokenizes remaining lexemes
                        if __lexeme != "":
                            self.tokenize(__lexeme)
                            __lexeme = ""

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
                        self.comment_line = 0
                        self.comment_start = 0
                        __oplexeme = ""

                # Checks if character is a substring of the terminator of multiline comments
                if char == "*" or char == "/":
                    __oplexeme += char

        # Checks whether there is an unterminated multi-line comment, character, and string
        if self.multiComment:
            print(f"\033[91mERROR: MultiLine Comment not concluded in character {self.comment_start}, line {self.comment_line}.\033[0m")
        
        if self.isChar:
            print(f"\033[91mERROR: Char literal is not terminated in character {self.char_start}, line {self.char_line}.\033[0m")

        if self.isString:
            print(f"\033[91mERROR: String literal is not terminated in character {self.string_start}, line {self.string_line}.\033[0m")

    def tokenize(self, lexeme: str):
        """
        Determines the token of each lexeme.
        """
        if lexeme in KEYWORDS:
            self.tokenized_list.append([str(self.line_count), lexeme, KEYWORDS[lexeme]])
        
        elif lexeme in NOISEWORDS:
            self.tokenized_list.append([str(self.line_count), lexeme, NOISEWORDS[lexeme]])

        elif lexeme in OP_ASSIGNMENT:
            self.tokenized_list.append([str(self.line_count), lexeme, OP_ASSIGNMENT[lexeme]])

        elif lexeme in OP_ARITHMETIC:
            self.tokenized_list.append([str(self.line_count), lexeme, OP_ARITHMETIC[lexeme]])

        elif lexeme in OP_UNARY:
            self.tokenized_list.append([str(self.line_count), lexeme, OP_UNARY[lexeme]])

        elif lexeme in OP_RELATION:
            self.tokenized_list.append([str(self.line_count), lexeme, OP_RELATION[lexeme]])

        elif lexeme in DELIMITERS:
            self.tokenized_list.append([str(self.line_count), lexeme, DELIMITERS[lexeme]])

        elif lexeme in ESCAPE_SEQUENCES:
            self.tokenized_list.append([str(self.line_count), lexeme, ESCAPE_SEQUENCES[lexeme]])

        elif lexeme in COMMENTS:
            self.tokenized_list.append([str(self.line_count), lexeme, COMMENTS[lexeme]])
        
        elif lexeme.isnumeric():
            self.tokenized_list.append([str(self.line_count), lexeme, "INT_LITERAL"])

        elif len(lexeme) > 1 and (lexeme[-1] == "f") and (lexeme[-2] != ".") and self.isfloat(lexeme.replace("f", "")):
            self.tokenized_list.append([str(self.line_count), lexeme, "FLOAT_LITERAL"])

        elif len(lexeme) > 1 and ("." in lexeme) and (lexeme[-1] != ".") and self.isfloat(lexeme):
            self.tokenized_list.append([str(self.line_count), lexeme, "DOUBLE_LITERAL"])

        elif lexeme[0] == "\"" and lexeme[-1] == "\"":
            self.tokenized_list.append([str(self.line_count), lexeme, "STRING_LITERAL"])

        elif lexeme[0] == "\'" and lexeme[-1] == "\'":
            if len(lexeme.replace("\'", "")) == 1:
                self.tokenized_list.append([str(self.line_count), lexeme, "CHAR_LITERAL"])
            else:
                print(f"\033[91mERROR: Invalid Character Literal at character {self.char_count-1} line {self.line_count}.\033[0m")
                self.tokenized_list.append([str(self.line_count), lexeme, "UNKNOWN_TOKEN"])

        else:
            if len(lexeme) > 0 and lexeme[0].isalpha() and lexeme.replace("_", "").isalnum():
                self.tokenized_list.append([str(self.line_count), lexeme, "IDENTIFIER"])
            else:
                print(f"\033[91mERROR: Unknown Token at character {self.char_count-1}, line {self.line_count}.\033[0m")
                self.tokenized_list.append([str(self.line_count), lexeme, "UNKNOWN_TOKEN"])

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
        display_list.extend(self.tokenized_list)

        print(f"SYMBOL TABLE for {self.file_path}")
        print(f"Total Tokenized Lexemes:\t{len(self.tokenized_list)}\n")

        for lexeme in display_list:
            length_1 = len(lexeme[0])
            length_2 = len(lexeme[1])
            if (length_1 > longest_1):
                longest_1 = length_1
            
            if (length_2 > longest_2):
                longest_2 = length_2

        for lexeme in display_list:
            spacing_1 = ((longest_1 - len(lexeme[0])) + 2) * " "
            spacing_2 = ((longest_2 - len(lexeme[1])) + 20) * " "
            print(lexeme[0], spacing_1 + "|", lexeme[1], spacing_2 + "|", lexeme[2])

    def generatefile(self):
        """
        Generates the symbol table of the source code
        """
        PDF_TABLE = [["LINE", "LEXEME", "TOKEN"]]
        PDF_TABLE.extend(self.tokenized_list)

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Inconsolata", "",
                     fname="C:\\Users\\xcharuzu\\Documents\\GitHub\\luseed\\font\\Inconsolata-Regular.ttf",
                     uni=True)
        
        pdf.add_font("Inconsolata", "B",
                     fname="C:\\Users\\xcharuzu\\Documents\\GitHub\\luseed\\font\\Inconsolata-Bold.ttf",
                     uni=True)
        
        pdf.set_font("Inconsolata", "B", size=16)
        pdf.cell(text="SYMBOL TABLE for " + self.file_path, ln=1, center=True)
        pdf.set_font("Inconsolata", "", size=12)
        pdf.cell(text=" ", ln=1)
        pdf.cell(text="Total Tokenized Lexemes: " + str(len(self.tokenized_list)), ln=1)
        pdf.cell(text="Elapsed Time:            " + self.elapsed_time, ln=1)
        pdf.cell(text=" ", ln=1)
        with pdf.table(col_widths=(15, 40, 40)) as table:
            for data_row in PDF_TABLE:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        pdf.output(name='src/symboltable/SYMBOL_TABLE_' + self.file_path + ".pdf", dest="F")

    def returntokens(self):
        """
        Returns the tokens found in the file.
        """
        return self.tokenized_list