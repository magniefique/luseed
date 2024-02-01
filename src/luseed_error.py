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
        INVALID_STMNT = "Cannot start a statement with "
        EXPRESSION_STMNT = "Cannot use a value/expression/identifer as a statement"
        ELIF_ERROR = "Cannot  use \'elif\' without previous \'if\' statement"
        ELSE_ERROR = "Cannot  use \'else\' without previous \'if\' statement"
        INVALID_ASSIGN = "Expression cannot be an assignment statement"
        INVALID_PAREN = "Used a closing parenthesis \')\' without opening one"
        MISSING_LPAREN = "Expecting left parenthesis \'(\' at line "
        MISSING_RPAREN = "Expecting right parenthesis \')\' at line "
        MISSING_RSQUARE = "Expecting right square bracket \']\' at line "
        MISSING_OPERAND = "Expecting a value or an identifier at line "
        MISSING_SEMICOLON = "Expecting a statement terminator \';\' at line "
        EXPECTING_DEC = "Expecting \'[\', \'=\', or \';\' at line "
        EXPECTING_UN = "Expecting \'++\' or \'--\' at line "
        EXPECTING_IDEN = "Expecting identifier at line "
        INVALID_VALUE = "Invalid value found at line "
        
        def __init__(self, prompt: str = None, line_info: str = None) -> None:
            self.prompt = prompt
            self.line_info = line_info

        def displayerror(self):
            print(f"\033[91m[SyntaxError]: Syntax analyzer found an error within the source code:\n\t{self.prompt}.")
            print(f"\t{self.line_info}\033[0m")
            exit(1)