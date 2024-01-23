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
        res = self.frth_prec()
        print(res)

    def factor(self):
        curr_tok = self.current_token

        if curr_tok.token in NUM_DATA or curr_tok.token == "IDENTIFIER":
            self.idx_advance()
            return TokenRep(curr_tok)

        if curr_tok.token == "DELIM_OPEN_PRNTHSIS":
            self.idx_advance()
            res = self.frth_prec()
            if self.current_token.token == "DELIM_CLOSE_PRNTHSIS":
                self.idx_advance()
                return res

    def frst_prec(self):
        return self.binary_op(self.factor, OP_FRSTPREC)

    def sec_prec(self):
        return self.binary_op(self.frst_prec, OP_SECPREC)

    def thrd_prec(self):
        return self.binary_op(self.sec_prec, OP_THRDPREC)

    def frth_prec(self):
        return self.binary_op(self.thrd_prec, OP_FRTHPREC)

    def binary_op(self, func, ops):
        left_node = func()

        while self.current_token.token in ops:
            op_tok = TokenRep(self.current_token)
            self.idx_advance()
            right_node = func()
            left_node = BinaryOpNode(left_node, op_tok, right_node)

        return left_node