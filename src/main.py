from tokens import *
from lexerver2 import *
from syntax import *

def readfile(file_path: str):
    """
    This function reads the file and performs lexical analysis.
    """
    if file_path.endswith('.lsed'):
        # Read the file content
        file_content = ""
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        # Create a Lexer object and tokenize the file content
        code = Lexer(file_content, file_path)
        token_list = code.returntokens()
        #SyntacticAnalyzer(token_list)
        
    else:
        print(f"\033[91mERROR: Unsupported File Extension.\033[0m")
   
if __name__ == "__main__":
    # Get the file path from the user
    file_path = input("\033[93mluseed >\033[0m ")
    
    # Call the readfile function with the file path
    readfile(file_path)