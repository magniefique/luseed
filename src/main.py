
from tokens import *
from lexer import *
from syntax import *
import regex

# Function that reads the file 
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
        code = Lexer(file_content)
        token_list = code.returntokens()
        
        # Create a SyntacticAnalyzer object and perform syntactic analysis
        # analyzer = SyntacticAnalyzer(token_list)
        # analyzer.analyze()

    else:
        print(f"\033[91mERROR: Unsupported File Extension.\033[0m")
   
if __name__ == "__main__":
    # Get the file path from the user
    file_path = input("\033[93mluseed >\033[0m ")
    
    # Call the readfile function with the file path
    readfile(file_path)