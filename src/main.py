from tokens import *
from lexer import *
from pathlib import Path

def readfile(file_path: str):
    """
    This function reads the file and performs lexical analysis.
    """
    if Path(file_path).suffix == ".lsed":
        # Read the file content
        file_content = ""
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        # Create a Lexer object and tokenize the file content
        code = Lexer(file_content, file_path)
        token_list = code.returntokens()
        
    else:
        # Print error message if the file ends with other file extension
        print(f"\033[91mERROR: Unsupported File Extension ({Path(file_path).suffix}).\033[0m")
   
if __name__ == "__main__":
    # Get the file path from the user
    file_path = input("\033[93mluseed >\033[0m ")
    
    # Call the readfile function with the file path
    readfile(file_path)
