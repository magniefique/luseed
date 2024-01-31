from lexer.luseed_tokens import *
from lexer.luseed_token import *
from luseed_error import *
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

        self.space_len = 0
        self.char_cmnt_ctr = 0

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
        self.parse_code()
        end = time.time()

        # Computes for the Elapsed Time
        self.elapsed_time = str(end - start)

        # Returns tokens
        self.return_tokens()

    def parse_code(self):
        """
        Parses each character in the .lusd code.
        """
        self.line_count = 1

        for char in self.source_code:
            self.char_count += 1

            # Checks for whitespace characters
            if char in WHITESPACES:
                self.parse_white(char)
            
            # Checks if next character/s are not part of a comment
            if not self.singleComment and not self.multiComment:
                # Checks if next character/s are not part of a String literal or Char literal
                if not self.isString and not self.isChar:
                    if char.isalnum():
                        self.parse_alnum(char)

                    elif char in SPECIAL_CHAR:
                        self.parse_spec(char)
                
                # Checks if next character is part of a Char literal
                elif self.isChar:
                    self.parse_char(char)

                # Checks if next character/s are not part of a String literal
                elif self.isString:
                    self.parse_string(char)

            # Checks if the following character/s is a part of a single-line comment
            elif self.singleComment:
                self.parse_comment(char, "single")

            # Checks if the following character/s is a part of a multi-line comment
            elif self.multiComment:
                self.parse_comment(char, "multi")
        
        
        self.reset_buffers("lexeme")
        self.reset_buffers("oplexeme_2")

        self.error_check(1)

    def parse_alnum(self, char: str):
        """
        Responsible for parsing alphanumeric characters.
        """
        if self.lexeme == ".":
            self.tokenize(self.lexeme)
            self.lexeme = ""

        self.lexeme += char
                    
        # Appends the current value of the self.oplexeme if it is not empty 
        if self.oplexeme != "" and self.lexeme != "":
            if self.oplexeme == "+-" or self.oplexeme == "-+":
                self.tokenize(self.oplexeme[0])
                self.tokenize(self.oplexeme[1])

            else:
                self.tokenize(self.oplexeme)
            
            self.oplexeme = ""

    def parse_spec(self, char: str):
        """
        Responsible for parsing special characters
        """
        # Checks if char is part of an operator that contains 2 characters
        if char in DOUBLE_OP:
            # Tokenizes the lexemes present in the self.lexeme
            self.reset_buffers("lexeme")
            
            self.oplexeme += char

            # Activates comment boolean if self.oplexeme is in comments
            if self.oplexeme in COMMENTS:
                if self.oplexeme == "//":
                    self.singleComment = True

                elif self.oplexeme == "/*":
                    self.multiComment = True
                    self.char_cmnt_ctr = 2
                    self.comment_line = self.line_count
                    self.comment_start = self.char_count

                self.lexeme += self.oplexeme
                self.oplexeme = ""
               
        else:
            # Appends the current value of the self.oplexeme if it is not empty 
            if (self.oplexeme == "+-" or self.oplexeme == "-+" or self.oplexeme == "++" or self.oplexeme == "--") and (char != ";" and char != ")"):
                self.tokenize(self.oplexeme[0])
                self.tokenize(self.oplexeme[1])
                self.oplexeme = ""

            else:
                self.reset_buffers("oplexeme_1") 

            # Checks if character is a double quotation for str literals
            if char == "\"":
                self.string_line = self.line_count
                self.string_start = self.char_count
                self.lexeme += char
                self.isString = True

            # Checks if character is a single quotation for char literals
            elif char == "\'":
                self.char_line = self.line_count
                self.char_start = self.char_count
                self.lexeme += char
                self.isChar = True
            
            # Checks if char is a period 
            elif char == ".":
                # Checks if the contents of the self.lexeme is numeric for floating-point values
                if self.lexeme.isnumeric() or self.lexeme == "":
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
                self.reset_buffers("lexeme")

                # Parses the operator present in self.oplexeme
                self.reset_buffers("oplexeme_1")

                # Sets the current char to self.lexeme and turns it into a lexeme
                self.tokenize(char)

    def parse_white(self, char: str):
        """
        Responsible for parsing whitespaces
        """
        # Checks if the current character is a new line character
        if char == "\n":
            if self.singleComment:
                self.singleComment = False
                self.reset_buffers("lexeme")
            
            if self.multiComment:
                self.check_len(self.char_cmnt_ctr)
                self.char_cmnt_ctr = 0
                return

            # Resets both Char and String when new line is introduced
            if self.isChar:
                self.tokenize(self.lexeme)
                self.error_check(2)
                self.isChar = False
                self.lexeme = "" 
            
            if self.isString:
                self.tokenize(self.lexeme)
                self.error_check(3)
                self.isString = False
                self.lexeme = ""

            # Tokenizes lexemes if they are not empty
            self.reset_buffers("lexeme")
            
            self.reset_buffers("oplexeme_2")

            self.tokenize(char)

            # Increments line count for new line and resets char cout
            self.line_count += 1
            self.char_count = 0
        
        elif char == " " and not self.isString and not self.singleComment and not self.multiComment:
            # Tokenizes lexemes if they are not empty
            self.reset_buffers("lexeme")
            
            self.reset_buffers("oplexeme_2")

    def parse_char(self, char: str):
        """
        Handles character literal values.
        """
        # Check if the current char is a double quote to terminate the char literal
        if char == "\'":
            self.lexeme += char
            self.tokenize(self.lexeme)
            self.lexeme = ""
            self.char_start = 0
            self.isChar = False

        else:
            self.lexeme += char
    
    def parse_string(self, char: str):
        """
        Handles string literal values.
        """
        # Checks if the next char value is used for an Escape Sequence (Ex. "\n")
        if self.isEscape:
            # Checks if character is not part of the ESCAPE_CHAR and return an error if true
            if char not in ESCAPE_CHAR:
                Error.TokenError(self.char_count, self.line_count, Error.TokenError.INVALID_ESC, True)

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
                self.string_start = 0
                self.isString = False

            # Check if the current char is a backslash to create an escape character/sequence
            elif char == "\\":
                self.oplexeme += char
                self.isEscape = True
            
            else:
                self.lexeme += char

    def parse_comment(self, char: str, type: str):
        if type == "single":
            self.lexeme += char

        elif type == "multi":
            # Checks if character is a substring of the terminator of multiline comments
            if char == "*" or char == "/":
                self.oplexeme += char
            
            else:
                self.lexeme += char

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
                    self.lexeme += self.oplexeme
                    self.reset_buffers("lexeme")
                    self.oplexeme = ""
                    self.check_len(self.char_cmnt_ctr)
                    self.char_cmnt_ctr = 0
                    return
            
            self.char_cmnt_ctr += 1

    def error_check(self, type: int):
        """
        Checks for unconcluded char, string, and multi-line comments.\n
        type = 1 | 2 | 3\n
        1 - Refers to Multi-Comment Errors\n
        2 - Refers to Unterminated Character Value\n
        3 - Referst to Unterminated String Value\n
        """
        if type == 1 and self.multiComment:
            Error.TokenError(self.comment_start, self.comment_line, Error.TokenError.UNTERMINATED_MULTICOMMENT)
        
        elif type == 2:
            Error.TokenError(self.char_start, self.char_line, Error.TokenError.UNTERMINATED_CHAR)

        elif type == 3:
            Error.TokenError(self.string_start, self.string_line, Error.TokenError.UNTERMINATED_STR)

    def reset_buffers(self, type: str):
        """
        Resets both lexeme and oplexeme.
        """
        if type == "lexeme":
            if self.lexeme != "":
                self.tokenize(self.lexeme)
                self.lexeme = ""
        
        elif type == "oplexeme_1":
            if self.oplexeme != "":
                self.tokenize(self.oplexeme)
                self.oplexeme = ""
        
        elif type == "oplexeme_2":
            if self.oplexeme != "":
                if (self.oplexeme != "*" or self.oplexeme != "/") and not self.multiComment:
                    self.tokenize(self.oplexeme)
                    self.oplexeme = ""

    def tokenize(self, lexeme: str):
        """
        Determines the token of each lexeme.
        """
        if lexeme in KEYWORDS:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, KEYWORDS[lexeme]))
        
        elif lexeme in NOISEWORDS:
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, KEYWORDS[NOISEWORDS[lexeme]]))

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

        elif lexeme in WHITESPACES:
            self.tokenized_lexemes.append(Token(self.line_count, WHITESPACE_REP[WHITESPACES[lexeme]], WHITESPACES[lexeme]))

        elif lexeme[:2] == "//" or (lexeme[:2] == "/*" and lexeme[-2:] == "*/") or lexeme[:2] == "/*":
            if lexeme[:2] == "//":
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, CMNT_SINGLE))
            
            else:
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, CMNT_MULTI))
                return
        
        elif lexeme.isnumeric():
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, LIT_INT))

        elif len(lexeme) > 1 and (lexeme[-1] == "f") and (lexeme[-2] != ".") and self.is_float(lexeme.replace("f", "")) and (float(lexeme.replace("f", "")) > -3.4e-38 and float(lexeme.replace("f", "")) < 3.4e+38):
            if "." not in lexeme:
                lexeme = lexeme.rstrip(lexeme[-1])
                lexeme += ".0f"
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, LIT_FLT))

        elif len(lexeme) > 1 and ("." in lexeme) and (lexeme[-1] != ".") and self.is_float(lexeme):
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, LIT_DBL))

        elif lexeme[0] == "\"" and lexeme[-1] == "\"":
            self.tokenized_lexemes.append(Token(self.line_count, lexeme, LIT_STR))

        elif lexeme[0] == "\'" and lexeme[-1] == "\'":
            if len(lexeme.replace("\'", "")) == 1:
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, LIT_CHAR))

            else:
                Error.TokenError(line_count= self.line_count, prompt=Error.TokenError.INVALID_CHAR)
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, UNKNOWN_TOKEN))

        else:
            if len(lexeme) > 0 and lexeme[0].isalpha() and lexeme.replace("_", "").isalnum() and lexeme[-1].isalnum():
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, IDENTIFIER))

            else:
                Error.TokenError(line_count= self.line_count, prompt=Error.TokenError.INVALID_TOKEN)
                self.tokenized_lexemes.append(Token(self.line_count, lexeme, UNKNOWN_TOKEN))

        self.check_len(len(lexeme))

    def is_float(self, value):
        """
        Tests a value if it is a valid float
        """
        try:
            float(value)
            return True
        
        except ValueError:
            return False

    def check_len(self, lex_len: int):
        """
        Finds the longest lexeme
        """
        if (lex_len > self.space_len):
            self.space_len = lex_len

    def display_table(self, type: str = "console"):
        """
        Displays the Symbol Table in the Terminal\n
        type = "console" | "txt"\n
        "console" = Prints values in console.\n
        "txt" = Prints values in .txt file.\n
        "pdf" = Prints values in .pdf file.\n
        "all" = Prints values in all formats.
        """

        if type == "console":
            print(f"\n\033[1mSYMBOL TABLE for {self.file_path}\033[0m")
            print(f"Total Tokenized Lexemes\t\t: {len(self.tokenized_lexemes)}")
            print(f"Elapsed Time\t\t\t: {self.elapsed_time}\n")
        
        elif type == "txt":
            file = open(f'src\symboltable_txt\SYMBOL_TABLE_{self.file_path}', 'w')
            file.write(f"\nSYMBOL TABLE for {self.file_path}" + "\n")
            file.write(f"Total Tokenized Lexemes\t\t: {len(self.tokenized_lexemes)}" + "\n")
            file.write(f"Elapsed Time\t\t\t\t: {self.elapsed_time}" + "\n")
        
        elif type == "pdf":
            self.generate_file()
            return
        
        elif type == "all":
            self.display_table("console")
            self.display_table("txt")
            self.generate_file()
            return

        else:
            Error.OutputError(type, Error.OutputError.INVALID_OUTPUT).displayerror()
            return

        longest_1 = 0
        longest_2 = 0

        display_str =''

        display_list = [["LEXEME", "LINE", "TOKEN"]]
        display_list.extend(self.tokenized_lexemes)

        # Calculates length of lexeme
        if self.space_len > len(display_list[0][0]):
            longest_1 = self.space_len
        
        else:
            len(display_list[0][0])

        if len(str(len(self.tokenized_lexemes))) > len(display_list[0][1]):
            longest_2 = len(str(len(self.tokenized_lexemes)))
        
        else:
            len(display_list[0][0])

        if type == "console":
            print(f"|------------------------START OF SYMBOL TABLE------------------------|\n")
            
        elif type == "txt":
            file.write(f"|------------------------END OF SYMBOL TABLE------------------------|" + '\n')

        # Displays the symbol table in the console
        for i in range(len(display_list)):
            if i == 0:
                spacing_1 = (longest_1 + 10)
                spacing_2 = (longest_2 + 20)

                if type == "console":
                    display_str = f"\033[1m{display_list[i][0]:<{spacing_1}}\033[0m\033[1m{display_list[i][1]:<{spacing_2}}\033[0m\033[1m{display_list[i][2]}\033[0m"

                elif type == "txt":
                    display_str = f"{display_list[i][0]:<{spacing_1}}{display_list[i][1]:<{spacing_2}}{display_list[i][2]}"

            else:
                spacing_1 = (longest_1 + 10)
                spacing_2 = (longest_2 + 20)
                offset = display_list[i].lexeme.rfind("\n")
                new_spacing = spacing_1 + offset + 1 if offset != -1 else spacing_1
                display_str = f"{display_list[i].lexeme:<{new_spacing}}{display_list[i].line:<{spacing_2}}{display_list[i].token}"
            
            if type == "console":
                print(display_str)
            
            elif type == "txt":
                file.write(display_str + '\n')

        if type == "console":
            print(f"\n|-------------------------END OF SYMBOL TABLE-------------------------|\n")
            
        elif type == "txt":
            file.write(f"\n|-------------------------END OF SYMBOL TABLE-------------------------|" + '\n')

        if type == "txt":
            print(f"The SYMBOL_TABLE_{self.file_path}.txt has been generated.")
        
        return

    def generate_file(self):
        """
        Generates the symbol table of the source code
        """
        PDF_TABLE = [["LINE", "LEXEME", "TOKEN"]]
        PDF_TABLE.extend(self.tokenized_lexemes)

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Inconsolata", "",
                     fname="font\\Inconsolata-Regular.ttf",
                     uni=True)
        
        pdf.add_font("Inconsolata", "B",
                     fname="font\\Inconsolata-Bold.ttf",
                     uni=True)
        
        pdf.set_font("Inconsolata", "B", size=16)
        pdf.cell(txt="SYMBOL TABLE for " + self.file_path, ln=1, center=True)
        pdf.set_font("Inconsolata", "", size=12)
        pdf.cell(txt=" ", ln=1)
        pdf.cell(txt="Total Tokenized Lexemes :" + str(len(self.tokenized_lexemes)), ln=1)
        pdf.cell(txt="Elapsed Time            :" + self.elapsed_time, ln=1)
        pdf.cell(txt=" ", ln=1)
        with pdf.table(col_widths=(15, 40, 40)) as table:
            for i in range(len(PDF_TABLE)):
                row = table.row()
                tkn_array = PDF_TABLE[i] if i == 0 else [PDF_TABLE[i].line, PDF_TABLE[i].lexeme, PDF_TABLE[i].token]
                
                for datum in tkn_array:
                    row.cell(datum)
                
        pdf.output(name='src/symboltable_pdf/SYMBOL_TABLE_' + self.file_path + ".pdf", dest="F")
        print(f"The SYMBOL_TABLE_{self.file_path}.pdf has been generated.")

    def return_tokens(self):
        """
        Returns the tokens found in the file.
        """
        return self.tokenized_lexemes