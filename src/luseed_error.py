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
                print(f"\033[91m[TokenError]: Invalid lexeme found in line {self.line_count}.\n\t{self.prompt}\033[0m")
            
            elif type == 2:
                print(f"\033[91m[TokenError]: Unterminated char/str/comment found in character {self.lexeme_start}, line {self.line_count}.\n\t{self.prompt}\033[0m") 

            elif type == 3:
                print(f"\033[91m[TokenError]: Error within string literal in character {self.lexeme_start}, line {self.line_count}.\n\t{self.prompt}\033[0m")

    class OutputError:
        INVALID_OUTPUT = "Invalid output method for the following symbol table."

        def __init__(self, output_style: str = None, prompt: str = None):
            self.output_style: str = output_style
            self.prompt: str = prompt
        
        def displayerror(self):
            print(f"\033[91m[OutputError]: Symbol Table cannot be presented.\n\t{self.prompt}\033[0m")