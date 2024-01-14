"""
Identifies the Token of the Lexeme
Credits to my friend Devian
"""

class Token:
    """
    Refers to the information about the Tokenized Lexeme
    """
    def __init__(self, line: int = None, lexeme: str = None, token: str = None) -> None:
        self.line: int = str(line)
        self.lexeme: str = lexeme
        self.token: str = token
    
    def __repr__(self) -> str:
        return f'[\'{self.line}\', \'{self.lexeme}\', \'{self.token}\']'
    
    def __str__(self) -> str:
        return f'[\'{self.line}\', \'{self.lexeme}\', \'{self.token}\']'