from luseed_tokens import *
from luseed_token import *
from luseed_error import *

class TokenRep:
    def __init__(self, token: Token):
        self.token = token
    
    def __repr__(self) -> str:
        return f"{self.token.token}:{self.token.lexeme}"

class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node  = left_node
        self.op_token = op_token
        self.right_node = right_node
    
    def __repr__(self) -> str:
        return f"({self.left_node}, {self.op_token}, {self.right_node})"

class UnaryNode:
    def __init__(self, unary_op, node):
        self.unary_op = unary_op
        self.node = node

    def __repr__(self) -> str:
        return f"({self.unary_op.token}:{self.unary_op.lexeme}, {self.node})"

class Parser:
    def __init__(self, token_list: list):
        self.token_list = token_list
        self.idx_ctr = -1
        self.idx_advance()
    
    def idx_advance(self):
        self.idx_ctr += 1
        if self.idx_ctr < len(self.token_list):
            self.current_token = self.token_list[self.idx_ctr]
        
        return self.current_token

    def parse(self):
        res = self.assign()
        print(res)

    def factor(self):
        curr_tok = self.current_token

        if curr_tok.token in UNARY:
            self.idx_advance()
            factor = self.factor()
            return UnaryNode(curr_tok, factor)

        elif curr_tok.token in NUM_DATA or curr_tok.token == "IDENTIFIER":
            self.idx_advance()
            return TokenRep(curr_tok)

        elif curr_tok.token == "DELIM_OPN_PRN":
            self.idx_advance()
            res = self.or_op()
            if self.current_token.token == "DELIM_CLS_PRN":
                self.idx_advance()
                return res

    def expntiate(self):
        return self.binary_op(self.factor, EXPONENTIATE)

    def multplctve(self):
        return self.binary_op(self.expntiate, MULTIPLICATIVE)

    def addtve(self):
        return self.binary_op(self.multplctve, ADDITIVE)

    def rlation(self):
        return self.binary_op(self.addtve, RELATION)
    
    def eqlity(self):
        return self.binary_op(self.rlation, EQUALITY)
    
    def and_op(self):
        return self.binary_op(self.eqlity, AND_OP)
    
    def or_op(self):
        return self.binary_op(self.and_op, OR_OP)
    
    def assign(self):
        return self.binary_op(self.or_op, ASSIGNMENT)

    def binary_op(self, func, ops):
        left_node = func()

        while self.current_token.token in ops:
            op_tok = TokenRep(self.current_token)
            self.idx_advance()
            right_node = func()
            left_node = BinaryOpNode(left_node, op_tok, right_node)

        return left_node