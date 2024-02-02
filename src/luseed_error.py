class Error:
    class FileError:
        INVALID_FILE = "File format not supported. Must be an .lusd file."
        FILE_NOT_FOUND = "File does not exist."
    
        def __init__(self, filepath: str, prompt: str = None):
            self.filepath: str = filepath
            self.prompt: str = prompt 

            self.displayerror()
        
        def displayerror(self):
            print(f"\033[91m[FileError]: File error in {self.filepath}.\n\t{self.prompt}\033[0m")

    class TokenError:
        INVALID_TOKEN = "Token for lexeme cannot be found."
        INVALID_CHAR = "Invalid Character Literal found."
        INVALID_ESC = "Invalid Escape Sequence found."
        UNTERMINATED_CHAR = "Unterminated Char Literal is prohibited."
        UNTERMINATED_STR = "Unterminated String Literal is prohibited."
        UNTERMINATED_MULTICOMMENT = "Unterminated Multi-Line Comment is prohibited."
        
        def __init__(self, lexeme_start: int = None, line_count: int = None, prompt: str = None, isesc: bool = False):
            self.prompt: str = prompt 
            self.lexeme_start: int = lexeme_start
            self.line_count: int = line_count

            if lexeme_start is None:
                self.displayerror(1)

            else:
                if isesc:
                    self.displayerror(3)

                else:
                    self.displayerror(2)
    
        def displayerror(self, type: int = None):
            if type == 1:
                print(f"\033[93m[Warning]: Invalid lexeme found in line {self.line_count}.\n\t{self.prompt}\033[0m")
            
            elif type == 2:
                print(f"\033[93m[Warning]: Unterminated char/str/comment found in character {self.lexeme_start}, line {self.line_count}.\n\t{self.prompt}\033[0m") 

            elif type == 3:
                print(f"\033[93m[Warning]: Error within string literal in character {self.lexeme_start}, line {self.line_count}.\n\t{self.prompt}\033[0m")

    class OutputError:
        INVALID_OUTPUT = "Invalid output method for the following symbol table."

        def __init__(self, output_style: str = None, prompt: str = None):
            self.output_style: str = output_style
            self.prompt: str = prompt
        
        def displayerror(self):
            print(f"\033[91m[OutputError]: Symbol Table cannot be presented.\n\t{self.prompt}\033[0m")
    
    class SyntaxError:
        UNKNOWN_TOKEN = "Unknown token found at line "
        INVALID_IMPORT = "Invalid import statement at line "
        INVALID_STMNT = "Cannot start a statement with "
        EXPRESSION_STMNT = "Cannot use a value/expression/identifer as a statement"
        ELIF_ERROR = "Cannot  use \'elif\' without previous \'if\' statement"
        ELSE_ERROR = "Cannot  use \'else\' without previous \'if\' statement"
        IN_ERROR = "Expecting an \'in\' keyword after a declaration"
        CATCH_ERROR = "Cannot  use \'catch\' without previous \'try\' statement"
        FINALLY_ERROR = "Cannot  use \'finally\' without previous \'try\' statement"
        IMPORT_ERROR = "Expecting an \'import\' keyword after identifier at line "
        IMPORT_IDEN_ERROR = "Expecting an identifier or \'all\' keyword at line "
        INVALID_ASSIGN = "Expression cannot be an assignment statement"
        INVALID_PAREN = "Used a closing parenthesis \')\' without opening one"
        EXPECTING_DATA_TYPE = "Expecting a data type (int, float, double, str, char, list, bool) at line "
        EXPECTING_LPAREN = "Expecting left parenthesis \'(\' at line "
        EXPECTING_RPAREN = "Expecting right parenthesis \')\' at line "
        EXPECTING_RSQUARE = "Expecting right square bracket \']\' at line "
        EXPECTING__LCURLY = "Expecting left curly bracket \'{\' at line "
        EXPECTING__RCURLY = "Expecting right curly bracket \'}\' at line "
        EXPECTING_OPERAND = "Expecting a value or an identifier at line "
        EXPECTING_SEMICOLON = "Expecting a statement terminator \';\' at line "
        EXPECTING_DEC = "Expecting \'[\', \'=\', or \';\' at line "
        EXPECTING_IDEN_STMNT = "Expecting \'[\', \'++\', \'--\', \'=\', or \';\' at line "
        EXPECTING_ACCESS_MOD = "Expecting data type, \'func\', or \'class\' at line "
        EXPECTING_UN = "Expecting \'++\' or \'--\' at line "
        EXPECTING_OP = "Expecting an operator at line "
        EXPECTING_SEP = "Expecting a comma \',\' at line "
        EXPECTING_COLON = "Expecting a colon \':\' at line "
        EXPECTING_ASSIGN = "Expecting an assignment operator \'=\', \'+=\', \'-=\', \'*=\', \'/=\', \'%=\', \'~=\' at line "
        EXPECTING_LOOP = "Expecting a loop statement"
        EXPECTING_IDEN = "Expecting identifier at line "
        EXPECTING_VAL = "Expecting a value at line "
        EXPECTING_THEN = "Expecting keyword 'then' after the condition"
        EXPECTING_UNTIL = "Expecting keyword 'until' after the code block"
        EXPECTING_ERROR = "Expecting an Error at line " 
        EXPECTING_CATCH = "Expecting keyword 'catch' after the try statement" 
        INVALID_EXPR_PAREN = "Expressional parentheses cannot be empty"
        INVALID_VALUE = "Invalid value found at line "
        THIS_ERROR = "The \"this\" keyword cannot be used as an identifier in this context"
        
        def __init__(self, prompt: str = None, token: str = None, line_list: list = None) -> None:
            self.prompt = prompt
            self.token = token
            self.line_info = int(token.line)
            self.line_list = line_list

        def displayerror(self):
            print(f"\033[91m[SyntaxError]: Syntax analyzer found an error within the source code:\n\t{self.prompt}.")
            print(f"\033[0m\t{self.line_list[self.line_info - 1]}\033[0m")
            
            if self.token.token not in ["WHT_NEWLINE", "EOF"]:
                i = self.line_list[self.line_info - 1].rfind(self.token.lexeme)
                spaces = i * " "
                j = len(self.token.lexeme)
                indicator = j * "^"
                print(f"\033[93m\t{spaces}{indicator}")
            
            else:
                i = len(self.line_list[self.line_info - 1])
                spaces =  i * " "
                print(f"\033[93m\t{spaces}^")
            print(f"\033[91m\tParsing process halted.\033[0m")
            exit(1)