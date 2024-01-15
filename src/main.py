import os
import codecs
from luseed_tokens import *
from luseed_error import *
from lexer import *
from pathlib import Path

def readfile(file_path: str):
    """
    This function reads the file and performs lexical analysis.
    """
    if Path(file_input).suffix == ".lusd":
        # Read the file content
        file_content = ""
        cwd = os.getcwd()
        file_path = os.path.join(cwd, file_input)

        try:
            with codecs.open(file_path, 'r') as file:
                file_content = file.read()
                file_name = os.path.basename(file.name)
            # Create a Lexer object and tokenize the file content
            code = Lexer(file_content, file_name)
            token_list = code.returntokens()

        except FileNotFoundError:
            # Print error message if file is not found
            print(file_path)
            Error.FileError(file_path, Error.FileError.FILE_NOT_FOUND)
    else:
        # Print error message if the file ends with other file extension
        Error.FileError(file_path, Error.FileError.INVALID_FILE)
   
if __name__ == "__main__":
    # Get the file path from the user
    file_input = input("\033[93mluseed >\033[0m ")
    
    # Call the readfile function with the file path
    readfile(file_input)
