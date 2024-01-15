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
        UNCLOSED_CHAR = "Unclosed Char Literal is prohibited."
        UNCLOSED_STR = "Unclosed String Literal is prohibited."
        UNCLOSED_MULTICOMMENT = "Unclosed Multi-Line Comment is prohibited."
        
        def __init__(self, lexeme_start: int = None, line_count: int = None, prompt: str = None):
            self.prompt: str = prompt 
            self.lexeme_start: int = lexeme_start
            self.line_count: int = line_count

            if lexeme_start is None:
                self.displayerror(1)

            else:
                self.displayerror(2)
    
        def displayerror(self, type: int = None):
            if type == 1:
                print(f"\033[91m[TokenError]: Invalid lexeme found in line {self.line_count}.\n\t{self.prompt}\033[0m")
            
            elif type == 2:
                print(f"\033[91m[TokenError]: Unclosed char/str/comment found in character {self.lexeme_start}, line {self.line_count}.\n\t{self.prompt}\033[0m")    