
def readfile(file_path: str):
    if file_path.endswith('.lsed'):
        file_content = ""
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        Lexer(file_content)
    else:
        print("ERROR: Unsupported File Extension.")
    
if __name__ == "__main__":
    file_path = input("luseed > ")
    readfile(file_path)