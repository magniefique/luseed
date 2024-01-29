from lexer.luseed_token import *
from parser.grammar import *

class Node:
    """
    Node Representation of Each Token in a Tree
    """
    def __init__(self, token: Token):
        self.token = token
    
    def __repr__(self) -> str:
        return f'[{self.token.token}]:{self.token.lexeme}'

class TreeSegment:
    """
    Segment of the tree that contains the root node, the left node, and the right node
    """
    def __init__(self, left_node: Node, root_node: Node, right_node: Node):
        self.left_node = left_node
        self.root_node = root_node
        self.right_node = right_node
    
    def __repr__(self):
        if self.right_node == None and self.left_node != None:
            return f'({self.left_node}, {self.root_node})'

        elif self.right_node != None and self.left_node == None:
            return f'({self.root_node}, {self.right_node})'

        elif self.right_node == None and self.left_node == None:
            return f'{self.root_node}'

        else:
            return f'({self.left_node}, {self.root_node}, {self.right_node})'
    
class Parser:
    """
    Parses the tokens provided by the syntax analyzer.
    """
    def __init__(self, tk_list: list):
        self.tk_list = tk_list
        self.idx_ctr = -1
        self.is_done = False
        self.idx_incr()
    
    def idx_incr(self):
        self.idx_ctr += 1
        if self.idx_ctr < len(self.tk_list):
            self.curr_tok = self.tk_list[self.idx_ctr]
            self.look_for(["UNKNOWN_TOKEN"], self.curr_tok, "UNKNOWN TOKEN FOUND", False)
            
        else:
            if self.curr_tok.token not in ["WHT_NEWLINE", "DLM_RCURLY"]:
                self.look_for(["DLM_TRMNTR"], self.curr_tok, f"{self.curr_tok.lexeme} <- Missing statement terminator \';\'.", True) # Check if final char is semicolon

            self.is_done = True
            self.curr_tok = Token(None, " ",  "EOF")
            return

        return self.curr_tok

    def look_for(self, token: list, tok: Token, error: str, accept: bool):
        """
        Look for a token. If true, look for it, if false, look against it.
        """
        if (accept and tok.token in token) or (not accept and tok.token not in token):
            return True
        
        print(error)
        exit(1)

    def parse(self):
        while not self.is_done:
            parse_res = self.stmnt()
            print(parse_res)

        print("Successful Parse!")

    def expr_parse(self):
        """
        Parses and expression.
        """
        res = self.expr_or()
        
        self.look_for(OP_ASSIGNMENT.values(), self.curr_tok, "EXPRESSION CANNOT BE AN ASSIGNMENT TARGET", False)
        self.look_for(["DLM_LPRN", "DLM_RPRN"], self.curr_tok, "Invalid Usage of ')'", False)

        if self.curr_tok.token in ["DLM_LPRN", "DLM_RPRN"]:
            raise Exception("STARTED A PARENTHESIS GRRRRRRRR")
        return res

    # Recursion function of each operation (LEVELED)
    def expr_or(self):
        return self.expr_operation(self.expr_and, EXPR_OR, 'L')
    
    def expr_and(self):
        return self.expr_operation(self.expr_eq, EXPR_AND, 'L')

    def expr_eq(self):
        return self.expr_operation(self.expr_rel, EXPR_EQ, 'L')

    def expr_rel(self):
        return self.expr_operation(self.expr_add, EXPR_REL, 'L')

    def expr_add(self):
        return self.expr_operation(self.expr_mul, EXPR_ADD, 'L')

    def expr_mul(self):
        return self.expr_operation(self.expr_un, EXPR_MUL, 'L')
    
    def expr_un(self):
        return self.expr_operation(self.expr_expo, EXPR_UN, 'L')

    def expr_expo(self):
        return self.expr_operation(self.atom, EXPR_EXPO, 'R')

    def atom(self):
        """
        Values that can be used an expression on. 
        """
        curr_tok = self.curr_tok

        # Used for literals
        if curr_tok.token in LIT_DATA:
            self.idx_incr()
            return curr_tok

        # Used for Identifiers, Properties, Function Calls, and Methods
        elif curr_tok.token in [IDENTIFIER, "KW_THIS"]:
            return self.rule_iden()

        # Used for parenthetical expressions
        elif curr_tok.token == "DLM_LPRN":
            res = self.expr_paren(self.atom_paren)
            self.idx_incr()
            return res
        
        # Error
        elif curr_tok.token == "DLM_RPRN":
            raise SyntaxError("Missing '\(\' parenthesis.") #####RETURNS IF PARENTHESIS WAS USED EXAMPLE (4 + )

        # Used for unary operators
        elif self.curr_tok.token in ["OP_PLUS", "OP_MINUS"]:
            if self.curr_tok.token == "OP_PLUS":
                self.curr_tok.token = "OP_POS"
            
            elif self.curr_tok.token == "OP_MINUS":
                self.curr_tok.token = "OP_NEG"

            return None
        
        # Checks if operand is not completed
        elif curr_tok.token in "DLM_TRMNTR":
            raise SyntaxError("Error Operation on Operand") ################################################RETURNS IF OPERAND NOT CONCLUDED
        
        # Checks for invalid tokens for atoms
        else:
            raise SyntaxError("Error Operand!") ################################################RETURNS IF ATOMS ARE NOT VALID ATOMS (EX. KEYWORDS)

    def atom_paren(self):
        """
        Contains the contents of a equation within a parenthesis which cannot be empty
        """
        self.look_for(["DLM_RPRN"], self.curr_tok, "CANNOT BE EMPTY", False)#### CANNOT BE EMPTY EX. () + 3
        return self.expr_or()

    def expr_paren(self, func):
        """
        Function that handles different parenthetical expressions
        """
        self.look_for(["DLM_LPRN"], self.curr_tok, "Expected opening parenthesis", True)############
        self.idx_incr()
        res = func()
        self.look_for(["DLM_RPRN"], self.curr_tok, "MISSING RIGHT PARENTHESIS", True)################################ CANNOT BE MISSING A RIGHT PARENTHESIS
        return res

    def expr_operation(self, func, acc_op: list, assoc: str):
        """
        Recursion Function for Operator Precedence
        """
        left_node = func()
        if self.curr_tok.token == "DLM_TRMNTR":
            return left_node
        
        # ERROR VALUES FOR PARENTHESIS AND VALUE LIST
        self.look_for(VALUE_LIST, self.curr_tok, f"Invalid operation on identifier {self.curr_tok}", False) #########CHECKS FOR THE NEXT OPERATOR ERROR IF: 3 3 + 3, IDEN IDEN * IDEN

        while self.curr_tok.token in acc_op:
            op_tok = self.curr_tok
            self.idx_incr()
            if self.curr_tok.token == "EOF":
                break
                
            if assoc == 'L':
                right_node = func()
            
            elif assoc == 'R':
                right_node = self.expr_parse()
            
            left_node = TreeSegment(left_node, op_tok, right_node)

        return left_node

    def rule_iden(self):
        """
        Identifier Rules
        """
        iden_tok = self.curr_tok
        self.idx_incr()
        
        if self.curr_tok.token == "DLM_OBJECT":
            left_node = iden_tok
            
            while self.curr_tok.token == "DLM_OBJECT":
                self.look_for([IDENTIFIER], self.curr_tok, "Missing operand", False)
                root_node = self.curr_tok
                right_node = self.obj_atom()
                left_node = TreeSegment(left_node, root_node, right_node)
            
            return left_node

        elif self.curr_tok.token == "DLM_LPRN":    
            left_node = self.curr_tok
            root_node = self.expr_paren(self.args_list)
            right_node = self.curr_tok
            ret_val = TreeSegment(left_node, root_node, right_node)
            self.idx_incr()
            self.look_for(OP_ASSIGNMENT.values(), self.curr_tok, "Cannot assign value to an expression", False)
            return TreeSegment(None, iden_tok, ret_val)

        elif self.curr_tok.token in OP_ASSIGNMENT.values():
            return self.assign_stmnt(iden_tok)

        return iden_tok

    def args_list(self):
        arg_list = self.curr_tok
        if arg_list.token in LIT_DATA or arg_list.token == IDENTIFIER:
            return self.expr_operation(self.args_atom, ['DLM_SPRTR'], 'L')

        elif arg_list.token == "DLM_RPRN":
            return None

        else:
            raise SyntaxError("INVALID ARGUMENT")

    def args_atom(self):
        curr_tok = self.curr_tok

        if curr_tok.token in LIT_DATA:
            self.idx_incr()
            return curr_tok

        elif curr_tok.token == IDENTIFIER:
            return self.rule_iden()
        
        elif curr_tok.token == "DLM_RPRN":
            raise SyntaxError("UNFINISHED COMMA")##############################################

    def obj_atom(self):
        self.idx_incr()
        curr_tok = self.curr_tok

        self.look_for([IDENTIFIER], curr_tok, "Expecting Identifier", True)
        return self.rule_iden()
    
    def check_order(self, order_array):
        stmnt_list = []
        stmnt_order = order_array

        for i in stmnt_order:
            self.idx_incr()
            self.look_for(i[0], self.curr_tok, i[1], i[2])
            stmnt_list.append(self.curr_tok)
        
        return stmnt_list

#region Statements
    def stmnt(self):

        if self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()
            if self.curr_tok.token != "EOF":
                
                res = self.stmnt()
                return res

            else:
                return res

        # Mediator for the Simple Statements, Function Calls, and Method Calls.
        if self.curr_tok.token == IDENTIFIER:
            curr_stmnt = self.rule_iden()
            self.look_for(["DLM_TRMNTR"], self.curr_tok, "Missing ;", True)
            self.idx_incr()
            next_stmnt = self.stmnt()
            res = TreeSegment(None, curr_stmnt, next_stmnt)
            return res

        # Mediator for the import statements
        elif self.curr_tok.token in ["KW_IMPORT", "KW_FROM"]:
            curr_stmnt = self.imprt_stmnt()
            next_stmnt = self.stmnt()
            res = TreeSegment(None, curr_stmnt, next_stmnt)
            return res
    
        # Mediator for the main function
        elif self.curr_tok.token in ["KW_MAIN"]:
            curr_stmnt = self.prog_stmnt()
            next_stmnt = self.stmnt()
            res = TreeSegment(None, curr_stmnt, next_stmnt)
            return res

        elif self.curr_tok.token in ACCESS_MOD:
            modifier = self.curr_tok
            self.idx_incr()
            if self.curr_tok in DATA_TYPE:
                curr_stmnt = self.dec_stmnt()

    def assign_stmnt(self, dest_value):
        op = self.curr_tok
        self.idx_incr()
        value = self.expr_parse()
        self.look_for(["DLM_TRMNTR"], self.curr_tok, "Missing ; symbol", True)
        return TreeSegment(dest_value, op, value)

    # def assign_stmnt(self):
    #     dest_value = self.rule_iden(True)
    #     self.look_for(OP_ASSIGNMENT.values(), self.curr_tok,"Expecting Assignment Operator",  True)
    #     op = self.curr_tok
    #     self.idx_incr()
    #     value = self.expr_parse()
    #     self.look_for(["DLM_TRMNTR"], self.curr_tok, f"Missing ; ", True)
    #     self.idx_incr()
    #     return TreeSegment(dest_value, op, value)
    
    def imprt_stmnt(self):
        stmnt_stack = []
        stmnt_stack.append(self.curr_tok)

        if self.curr_tok.token == "KW_IMPORT":
            import_type = IMPORT_STMNT[0]
            
        elif self.curr_tok.token  == "KW_FROM":
            import_type = IMPORT_STMNT[1]

        stmnt_stack.extend(self.check_order(import_type))
        self.idx_incr()
        if import_type == IMPORT_STMNT[0]:
            return f'({stmnt_stack[0]}, {stmnt_stack[1]}, {stmnt_stack[2]})'
        
        elif import_type == IMPORT_STMNT[1]:
            return f'({stmnt_stack[0]}, {stmnt_stack[1]}, {stmnt_stack[2]}, {stmnt_stack[3]})'
        
    def prog_stmnt(self):
        """
        Parses the program statement of luseed. This is essential in running a lusd code.
        """
        sub_stmnt = None
        stmnt_stack = []
        stmnt_stack.append(self.curr_tok)
        
        stmnt_stack.extend(self.check_order(MAIN_STMNT))
        self.idx_incr()
        while self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()

        self.look_for(["DLM_LCURLY"], self.curr_tok,  "Missing '{' before code_block", True)
        lcurly = self.curr_tok
        self.idx_incr()
        while self.curr_tok.token != "DLM_RCURLY" and not self.is_done:
            sub_stmnt = self.stmnt()

        self.look_for(["DLM_RCURLY"], self.curr_tok,  "Missing '}' before code_block", True)
        rcurly = self.curr_tok
        self.idx_incr()

        stmnt_header = f'({stmnt_stack[0]}, {stmnt_stack[1]}, {stmnt_stack[2]}, {stmnt_stack[3]})'

        sub_stmnt = TreeSegment(lcurly, sub_stmnt, rcurly)
        return TreeSegment(None, stmnt_header, sub_stmnt)
#endregion