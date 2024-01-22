from luseed_tokens import *
from luseed_token import *
from luseed_error import *

class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
    
    def __repr__(self) -> str:
        return f"{self.token.token}:{self.token.lexeme}"

class OpNode:
    def __init__(self, left_node, op_token, right_node) -> None:
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

class SyntaxAnalyzer:
    """
    Analyzes the syntax of the code.
    """
    def __init__(self, token_list: list):
        self.token_list = token_list
        self.token_idx = 0
    
    def idx_increment(self):
        self.token_idx += 1
        if self.token_idx < len(self.token_list):
            self.current_token = self.token_list[self.token_idx]
        return self.current_token

    def num_literal(self):
        tok = self.current_token

        if tok.token in NUM_DATA:
            self.idx_increment()
            return NumberNode(tok)
    
    def arith_op(self, func: function, op: str):
        left = function()

        while (self.current_token in op):
            

    #####