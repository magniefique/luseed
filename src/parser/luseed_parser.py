from lexer.luseed_token import *
from parser.grammar import *

class TreeSegment:
    """
    Segment of the tree that contains the root node, the left node, and the right node
    """
    def __init__(self, left_node: Token, root_node: Token, right_node: Token):
        self.left_node = left_node
        self.root_node = root_node
        self.right_node = right_node
    
    def __repr__(self):
        if self.right_node == None and self.left_node != None:
            return f'({self.left_node}, {self.root_node})'

        elif self.right_node != None and self.left_node == None:
            return f'({self.root_node}, {self.right_node})'

        elif self.root_node == None:
            return f'({self.left_node}, {self.right_node})'

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
        self.debugger = 0
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

    def idx_dcr(self):
        self.idx_ctr -= 1

        self.curr_tok = self.tk_list[self.idx_ctr]
        return self.curr_tok

    def look_for(self, token: list, tok: Token, error: str, accept: bool):
        """
        Look for a token. If true, look for it, if false, look against it.
        """
        if (accept and tok.token in token) or (not accept and tok.token not in token):
            return tok
        
        print(error)
        exit(1)

    def parse(self):
        while not self.is_done:
            parse_res = self.stmnt()
            print(parse_res)

        print("\nSuccessful Parse!")

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
            if self.tk_list[self.idx_ctr + 1].token in DATA_TYPE:
                res = self.cast_stmnt()

            else:
                res = self.expr_paren(self.atom_paren)
                self.idx_incr()

            return res
        
        elif curr_tok.token == "DLM_LSQUARE":
            self.idx_incr()
            lsquare = curr_tok
            list_val = self.args_list()
            rsquare = self.look_for(["DLM_RSQUARE"], self.curr_tok, "Missing Right Square Bracket", True)
            self.idx_incr()
            return TreeSegment(lsquare, list_val, rsquare)

        # Used for unary operators
        elif self.curr_tok.token in ["OP_PLUS", "OP_MINUS"]:
            if self.curr_tok.token == "OP_PLUS":
                self.curr_tok.token = "OP_POS"
            
            elif self.curr_tok.token == "OP_MINUS":
                self.curr_tok.token = "OP_NEG"

            return None
        
        elif curr_tok.token == "KW_ASK":
            return self.input_expr(curr_tok)

        # Error
        elif curr_tok.token == "DLM_RPRN":
            raise SyntaxError("Missing '\(\' parenthesis.") #####RETURNS IF PARENTHESIS WAS USED EXAMPLE (4 + )

        # Checks if operand is not completed
        elif curr_tok.token in "DLM_TRMNTR":
            raise SyntaxError("Error Operation on Operand") ################################################RETURNS IF OPERAND NOT CONCLUDED
        
        # Checks for invalid tokens for atoms
        else:
            raise SyntaxError(f"Error Operand! {self.curr_tok}") ################################################RETURNS IF ATOMS ARE NOT VALID ATOMS (EX. KEYWORDS)

    def atom_paren(self):
        """
        Contains the contents of a equation within a parenthesis which cannot be empty
        """
        self.look_for(["DLM_RPRN"], self.curr_tok, "CANNOT BE EMPTY", False)#### CANNOT BE EMPTY EX. () + 3
        return self.expr_or()

    def expr_paren(self, func, is_op: bool = False):
        """
        Function that handles different parenthetical expressions
        """
        lparen = self.look_for(["DLM_LPRN"], self.curr_tok, "Expected opening parenthesis", True)############
        self.idx_incr()
        res = func()
        rparen = self.look_for(["DLM_RPRN"], self.curr_tok, f"MISSING RIGHT PARENTHESIS{self.curr_tok} {self.tk_list[self.idx_ctr-2]}", True)################################ CANNOT BE MISSING A RIGHT PARENTHESIS
        return res

    def expr_operation(self, func, acc_op: list, assoc: str):
        """
        Recursion Function for Operator Precedence
        """
        left_node = func()
        if self.curr_tok.token in ["DLM_TRMNTR", "WHT_NEWLINE"]:
            return left_node
        
        # ERROR VALUES FOR PARENTHESIS AND VALUE LIST
        self.look_for(VALUE_LIST, self.curr_tok, f"Invalid operation on value {self.curr_tok}, {self.tk_list[self.idx_ctr-1]}", False) #########CHECKS FOR THE NEXT OPERATOR ERROR IF: 3 3 + 3, IDEN IDEN * IDEN

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

        if iden_tok.token == "KW_THIS":
            self.look_for(["DLM_OBJECT"], self.curr_tok, "The \"this\" keyword cannot be used as an identifier in this context", True)

        if self.curr_tok.token == "DLM_OBJECT":
            left_node = iden_tok
            
            while self.curr_tok.token == "DLM_OBJECT":
                self.look_for([IDENTIFIER], self.curr_tok, "Missing operand", False)
                root_node = self.curr_tok
                right_node = self.obj_atom()
                left_node = TreeSegment(left_node, root_node, right_node)
            
            return left_node

        elif self.curr_tok.token == "DLM_LSQUARE":
            res = self.list_idx()
            return TreeSegment(None, iden_tok, res)

        return iden_tok

    def list_idx(self):
        lsquare = self.curr_tok
        self.idx_incr()
        if self.curr_tok.token in VALUE_LIST or self.curr_tok.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_NOT"]:
            idx_value = self.expr_or()
        
        else:
            raise SyntaxError("INVALID INDEX VALUE")

        rsquare = self.look_for(["DLM_RSQUARE"],  self.curr_tok, "Expected ']' to close index expression.", True)
        self.idx_incr()
        if self.curr_tok.token == "DLM_LSQUARE":
            res = TreeSegment(lsquare, idx_value, rsquare)
            next_idx = self.list_idx()
            res = TreeSegment(None, res, next_idx)
            return res
        
        return TreeSegment(lsquare, idx_value, rsquare)

    def args_list(self):
        arg_list = self.curr_tok
        if arg_list.token in VALUE_LIST or arg_list.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_NOT"]:
            return self.expr_operation(self.args_atom, ['DLM_SPRTR'], 'L')

        elif arg_list.token in ["DLM_RPRN", "DLM_RSQUARE"]:
            return None

        else:
            raise SyntaxError("INVALID ARGUMENT")

    def args_atom(self):
        self.look_for(["DLM_RPRN"], self.curr_tok, "Unfinished Comma", False)
        res = self.expr_or()
        return res

    def dec_atom(self):
        identifier = self.curr_tok
        self.idx_incr()

        if self.curr_tok.token == "DLM_LSQUARE":
            self.idx_dcr()
            identifier = self.rule_iden()

        if self.curr_tok.token in ["DLM_TRMNTR", "DLM_SPRTR"]:
            return identifier

        elif self.curr_tok.token == "OP_ASGN":
            op = self.curr_tok
            self.idx_incr()
            value = self.expr_parse()
            return TreeSegment(identifier, op, value)

        else:
            raise Exception(f"UNEXPECTED SYMBOL FOUND {self.curr_tok}")

    def param_list(self):
        return self.expr_operation(self.param_atom, ["DLM_SPRTR"], 'L')

    def param_atom(self):
        if self.curr_tok.token in DATA_TYPE:
            dataType = self.curr_tok
            self.idx_incr()
            identifier = self.look_for([IDENTIFIER], self.curr_tok, "Expecting Identifier", True)
            self.idx_incr()
            return  TreeSegment(None, dataType, identifier)
        
        elif self.curr_tok.token == "KW_THIS":
            kw_this = self.curr_tok
            self.idx_incr()
            return kw_this
        
        else:
            raise Exception("Invalid parameter")

    def obj_atom(self):
        self.idx_incr()
        self.look_for([IDENTIFIER], self.curr_tok, "Expecting Identifier", True)
        return self.rule_iden()
    
    def info_atom(self):
        if self.curr_tok.token in VALUE_LIST or self.curr_tok.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_NOT"]:
            return self.expr_or()
        
        elif self.curr_tok.token in KEYWORDS.values():
            res = self.curr_tok
            self.idx_incr()
            return res

    def swap_atom(self):
        atom_1 = self.look_for([IDENTIFIER], self.curr_tok, "Expected Identifier", True)
        self.idx_incr()
        sep_1 = self.look_for(["DLM_SPRTR"], self.curr_tok,  "Expected a separator", True)
        self.idx_incr()
        atom_2 = self.look_for([IDENTIFIER], self.curr_tok, "Expected Identifier", True)
        self.idx_incr()
        if self.curr_tok.token == "DLM_SPRTR":
            sep_2 = self.curr_tok
            self.idx_incr()
            atom_3 = self.look_for([IDENTIFIER], self.curr_tok, "Expected Identifier", True)
            self.idx_incr()
            return f'{atom_1}, {sep_1}, {atom_2}, {sep_2}, {atom_3}'
        
        elif self.curr_tok.token == "DLM_RPRN":
            return f'{atom_1}, {sep_1}, {atom_2}'

    def check_atom(self):
        self.look_for([IDENTIFIER], self.curr_tok, "Expecting an Identifier", True)
        iden = self.rule_iden()

        if self.curr_tok.token == "DLM_LPRN":
            lparen = self.curr_tok
            values = self.expr_paren(self.args_list)
            rparen = self.curr_tok
            self.idx_incr()
            return TreeSegment(lparen, values, rparen)

        return iden

    def for_expr(self):
        if self.curr_tok in DATA_TYPE:
            data_type = self.curr_tok
            self.idx_incr()
        
        iden = self.look_for([IDENTIFIER], self.curr_tok, "Expecting an Identifier", True)
        self.idx_incr()
        self.look_for(OP_ASSIGNMENT.values(), self.curr_tok, "Expecting assignment operation", True)
        init = self.assign_stmnt(iden)
        if self.curr_tok.token in VALUE_LIST or self.curr_tok.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_NOT"]:
            expr = self.expr_parse()

        else:
            raise Exception("Invalid value for expression")

        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "Expecting a delimiter ;", True)
        self.idx_incr()
        if self.curr_tok.token in OP_UNARY.values():
            update = self.unary_expr(None, 0)
        
        elif self.curr_tok.token == IDENTIFIER:
            update_iden = self.rule_iden()
            if self.curr_tok.token in OP_UNARY.values():
                update = self.unary_expr(update_iden, 1)
            
            elif self.curr_tok.token in OP_ASSIGNMENT.values():
                update = self.assign_expr(update_iden, False)

            else:
                raise Exception(f"Do you mean ++ or -- ? {self.curr_tok}")

        else:
            raise Exception("Invalid value for update section")

        condn = TreeSegment(None, expr, delim)
        return TreeSegment(init, condn, update)

    def error_atom(self):
        error = self.look_for([IDENTIFIER], self.curr_tok, "Expected an Identifier", True)
        self.idx_incr()
        return error

    def code_block(self, is_loop = False):
        self.idx_incr()
        if self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()

        lcurly = self.look_for(["DLM_LCURLY"], self.curr_tok,  "Missing '{' before code_block", True)
        self.idx_incr()
        while self.curr_tok.token != "DLM_RCURLY" and not self.is_done:
            sub_stmnt = self.stmnt(is_loop)

        rcurly = self.look_for(["DLM_RCURLY"], self.curr_tok,  "Missing '}' before code_block", True)
        self.idx_incr()

        return TreeSegment(lcurly, sub_stmnt, rcurly)

    def check_order(self, order_array):
        stmnt_list = []
        stmnt_order = order_array

        for i in stmnt_order:
            self.idx_incr()
            self.look_for(i[0], self.curr_tok, i[1], i[2])
            stmnt_list.append(self.curr_tok)
        
        return stmnt_list

#region Statements
    def stmnt(self, is_loop: bool=False):
        if self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()
            if self.curr_tok.token != "EOF" and self.curr_tok.token != "DLM_RCURLY":
                
                res = self.stmnt(is_loop)
                return res

            else:
                res = None
                return res

        # Mediator for the Simple Statements, Function Calls, and Method Calls.
        elif self.curr_tok.token in [IDENTIFIER, "KW_THIS"]:
            curr_stmnt = self.iden_stmnt()

        # Mediator for the import statements
        elif self.curr_tok.token in ["KW_IMPORT", "KW_FROM"]:
            curr_stmnt = self.imprt_stmnt()
    
        # Mediator for the main function
        elif self.curr_tok.token in ["KW_MAIN"]:
            curr_stmnt = self.prog_stmnt()

        elif self.curr_tok.token in DATA_TYPE:
            curr_stmnt = self.dec_stmnt()

        elif self.curr_tok.token in ["KW_DISPLAY", "KW_ASK"]:
            curr_stmnt = self.io_stmnt()
        
        elif self.curr_tok.token == "KW_IF":
            curr_stmnt = self.if_stmnt()

        elif self.curr_tok.token in ["KW_PASS", "KW_RETURN"]:
            curr_stmnt =  self.ctrl_stmnt()

        elif self.curr_tok.token in ["KW_BREAK",  "KW_CONTINUE"] and is_loop:
            curr_stmnt = self.ctrl_stmnt()

        elif self.curr_tok.token in OP_UNARY.values():
            curr_stmnt = self.unary_stmnt(None, 0)
        
        elif self.curr_tok.token == "KW_FUNC":
            curr_stmnt = self.func_stmnt()

        elif self.curr_tok.token == "KW_LOOP_FOR":
            curr_stmnt = self.for_stmnt()

        elif self.curr_tok.token == "KW_LOOP_WHILE":
            curr_stmnt = self.while_stmnt()

        elif self.curr_tok.token == "KW_LOOP_DO":
            curr_stmnt = self.do_stmnt()

        elif self.curr_tok.token == "KW_LOOP_REPEAT":
            curr_stmnt = self.repeat_stmnt()

        elif self.curr_tok.token == "KW_CLASS":
            curr_stmnt = self.class_stmnt()
        
        elif self.curr_tok.token == "KW_INIT":
            curr_stmnt = self.init_stmnt()

        elif self.curr_tok.token == "KW_RAISE":
            curr_stmnt = self.raise_stmnt()

        elif self.curr_tok.token == "KW_TRY":
            curr_stmnt = self.try_stmnt()

        elif self.curr_tok.token == "KW_INFO":
            curr_stmnt = self.info_stmnt()

        elif self.curr_tok.token == "KW_SWAP":
            curr_stmnt = self.swap_stmnt()

        elif self.curr_tok.token == "KW_CHECK":
            curr_stmnt = self.check_stmnt()

        elif self.curr_tok.token in ACCESS_MOD:
            modifier = self.curr_tok
            self.idx_incr()
            if self.curr_tok.token in DATA_TYPE:
                curr_stmnt = self.dec_stmnt()
                curr_stmnt = TreeSegment(None, modifier, curr_stmnt)
            
            elif self.curr_tok.token == "KW_FUNC":
                curr_stmnt = self.func_stmnt()
                curr_stmnt = TreeSegment(None, modifier, curr_stmnt)

            elif self.curr_tok.token == "KW_CLASS":
                curr_stmnt = self.class_stmnt()
                curr_stmnt = TreeSegment(None, modifier, curr_stmnt)
            
            curr_stmnt = (None, modifier, curr_stmnt)

        else:
            raise Exception(f"NONONONO WAY {self.curr_tok} {self.tk_list[self.idx_ctr - 2]}")

        if self.curr_tok.token != "DLM_RCURLY" and self.curr_tok.token != 'EOF':
            next_stmnt = self.stmnt(is_loop)
        
        else:
            next_stmnt = None

        res = TreeSegment(None, curr_stmnt, next_stmnt)
        return res

    def iden_stmnt(self):
        identifier = self.rule_iden()
        if self.curr_tok.token in OP_ASSIGNMENT.values():
            curr_stmnt = self.assign_stmnt(identifier)

        elif self.curr_tok.token == "DLM_LPRN":
            curr_stmnt = self.call_stmnt(identifier)

        elif self.curr_tok.token in OP_UNARY.values():
            curr_stmnt = self.unary_stmnt(identifier, 1)

        elif self.curr_tok.token == "DLM_TRMNTR":
            raise Exception("Expression cannot be a statement")
        
        return curr_stmnt  
    
    def call_stmnt(self, identifier):
        lparen = self.curr_tok
        args_val = self.expr_paren(self.args_list)
        rparen = self.curr_tok
        args = TreeSegment(lparen, args_val, rparen)
        self.idx_incr()
        self.look_for(OP_ASSIGNMENT.values(), self.curr_tok, "Cannot assign value to an expression", False)
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, f"Missing ; here {self.curr_tok}", True)
        self.idx_incr()
        return TreeSegment(identifier, args, delim)

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
        sub_stmnt = self.code_block()

        stmnt_header = f'({stmnt_stack[0]}, {stmnt_stack[1]}, {stmnt_stack[2]}, {stmnt_stack[3]})'

        return TreeSegment(None, stmnt_header, sub_stmnt)

    def dec_stmnt(self):
        data_type = self.curr_tok
        self.idx_incr()
        self.look_for([IDENTIFIER], self.curr_tok, "Expecting an Identifier", True)
        res = self.expr_operation(self.dec_atom, ["DLM_SPRTR"], 'L')
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok,  f"Expected ';' after declaration {self.curr_tok}", True)
        self.idx_incr()
        return TreeSegment(data_type, res, delim)

    def input_expr(self, keyword):
        kw_disp = keyword
        self.idx_incr()
        lparen = self.look_for(["DLM_LPRN"], self.curr_tok, "Expecting ( here ", True)
        args_list = self.expr_paren(self.args_list)
        rparen = self.look_for(["DLM_RPRN"], self.curr_tok, "Exprecting ) here", True)
        self.idx_incr()
        args = TreeSegment(lparen, args_list, rparen)
        return TreeSegment(None, kw_disp, args)

    def io_stmnt(self):
        kw_disp = self.curr_tok
        expr = self.input_expr(kw_disp)
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "Expected ; here", True)
        self.idx_incr()
        return TreeSegment(None, expr, delim)
    
    def assign_expr(self, dest_value, is_assign: bool = True):
        op = self.curr_tok
        self.idx_incr()
        self.look_for(["DLM_TRMNTR", "WHT_NEWLINE"], self.curr_tok, "Expecting a value after operator", False)
        value = self.expr_parse() if is_assign else self.expr_or()
        return TreeSegment(dest_value, op, value)

    def assign_stmnt(self, dest_value):
        expr = self.assign_expr(dest_value)
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, f"Missing ; symbol {self.curr_tok}", True)
        self.idx_incr()
        return TreeSegment (None, expr, delim)

    def func_stmnt(self):
        sub_stmnt = None
        stmnt_stack = []
        stmnt_stack.append(self.curr_tok)
        stmnt_stack.extend(self.check_order(FUNC_STMNT[0]))
        param_list = self.expr_paren(self.param_list)
        self.idx_dcr()
        stmnt_stack.extend(self.check_order(FUNC_STMNT[1]))
        sub_stmnt = self.code_block()
        param = TreeSegment(stmnt_stack[2],  param_list, stmnt_stack[3])
        header = f'{stmnt_stack[0]}, {stmnt_stack[1]}, {param}, {stmnt_stack[4]}'
        return TreeSegment(None, header, sub_stmnt)
    
    def condn_block(self, with_condn: bool = True):
        """
        Condition blocks for if/else statements.
        """
        kw_start = self.curr_tok
        self.idx_incr()
        if with_condn:
            lparen = self.curr_tok
            condn = self.expr_paren(self.atom_paren)
            rparen = self.curr_tok
            self.idx_incr()
            kw_then = self.look_for(["KW_THEN"], self.curr_tok, "Expecting then keyword after condition", True)
            self.idx_incr()

        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, "Expecting : symbol", True)
        sub_stmnt = self.code_block()
        # For if/elif statements
        if with_condn:
            condn_expr = TreeSegment(lparen, condn, rparen)
            inc_header = TreeSegment(kw_start, condn_expr, kw_then)
            condn_stmnt = TreeSegment(inc_header, colon, sub_stmnt)

        # For else statements
        else:
            condn_stmnt = TreeSegment(kw_start, colon, sub_stmnt)

        return condn_stmnt

    def if_stmnt(self):
        if_stmnt = self.condn_block()
        elif_stmnt = None
        else_stmnt = None

        while self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()

        if self.curr_tok.token == "KW_ELIF":
            elif_stmnt = self.elif_stmnt()
            if self.curr_tok.token == "KW_ELSE":
                else_stmnt = self.condn_block(False)
        
        elif self.curr_tok.token == "KW_ELSE":
            else_stmnt = self.condn_block(False)
        
        return TreeSegment(if_stmnt, elif_stmnt, else_stmnt)

    def elif_stmnt(self):
        elif_block = self.condn_block()
        while self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()
        while self.curr_tok.token == "KW_ELIF":
            next_elif = self.condn_block()
            elif_block = TreeSegment(None, elif_block, next_elif)
            while self.curr_tok.token == "WHT_NEWLINE":
                self.idx_incr()

        return elif_block

    def for_stmnt(self):
        kw_for = self.curr_tok
        self.idx_incr()
        lparen = self.curr_tok
        args_list = self.expr_paren(self.for_expr)
        rparen = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, "Expecting : after arguments", True)
        loop_body = self.code_block(True)

        args = TreeSegment(lparen, args_list, rparen)
        return f'{kw_for}, {args}, {colon}, {loop_body}'

    def while_stmnt(self):
        kw_while = self.curr_tok
        self.idx_incr()
        lparen = self.curr_tok
        condn = self.expr_paren(self.atom_paren)
        rparen = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, "Expected : after arguments", True)
        loop_body = self.code_block(True)
        args = TreeSegment(lparen, condn, rparen)
        return f'{kw_while}, {args}, {colon}, {loop_body}'

    def do_stmnt(self):
        kw_do = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, "Expected : after arguments", True)
        loop_body = self.code_block(True)
        if self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()
        kw_until = self.look_for(["KW_LOOP_UNTIL"], self.curr_tok, f"Expected 'Until' keyword {self.curr_tok}", True)
        self.idx_incr()
        lparen = self.curr_tok
        condn = self.expr_paren(self.atom_paren)
        rparen = self.curr_tok
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "Expected ;", True)
        self.idx_incr()
        args = TreeSegment(lparen, condn, rparen)
        header = TreeSegment(None, kw_do, colon)
        footer = TreeSegment(kw_until, args, delim)
        return TreeSegment(header, loop_body, footer)

    def repeat_stmnt(self):
        kw_repeat = self.curr_tok
        self.idx_incr()
        lparen = self.curr_tok
        rep_val = self.expr_paren(self.args_atom)
        rparen = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, "Expected : here", True)
        loop_body = self.code_block(True)
        args = TreeSegment(lparen, rep_val, rparen)
        return f'{kw_repeat}, {args}, {colon}, {loop_body}'

    def class_stmnt(self):
        kw_class = self.curr_tok
        parent = None
        self.idx_incr()
        iden = self.look_for([IDENTIFIER], self.curr_tok, "Expecting Identifier", True)
        self.idx_incr()
        if self.curr_tok.token == "DLM_LPRN":
            lparen = self.curr_tok
            iden = self.expr_paren(self.rule_iden)
            rparen = self.curr_tok
            self.idx_incr()
            parent = TreeSegment(lparen, iden, rparen)
        
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, f"Expecting : here {self.curr_tok}", True)
        class_body = self.code_block(False)
        class_name = TreeSegment(iden, parent, colon)
        return TreeSegment(kw_class, class_name, class_body)

    def init_stmnt(self):
        kw_init = self.curr_tok
        self.idx_incr()
        lparen = self.curr_tok
        param_list = self.expr_paren(self.param_list)
        rparen = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, "Expecting : after parameter list", True)
        sub_stmnt = self.code_block()
        param = TreeSegment(lparen, param_list, rparen)
        header = TreeSegment(kw_init, param, colon)
        return TreeSegment(None, header, sub_stmnt)

    def ctrl_stmnt(self):
        kw = self.curr_tok
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "Expected ; here", True)
        self.idx_incr()
        return  TreeSegment(None, kw, delim)
    
    def unary_expr(self, iden_value, un_type: int):
        if un_type == 0:
            unary_op = self.curr_tok
            self.idx_incr()
            iden = self.look_for([IDENTIFIER], self.curr_tok, "EXPECTED IDENTIFIER HERE", True)
            self.idx_incr()
            return TreeSegment(None, unary_op, iden)

        elif un_type == 1:
            iden = iden_value
            unary_op = self.look_for(OP_UNARY.values(), self.curr_tok, "Expected  Unary Operator Here", True)
            self.idx_incr()
            return TreeSegment(None, iden, unary_op)

    def unary_stmnt(self, iden_value = None, un_type: int = None):
        expr = self.unary_expr(iden_value, un_type)
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "EXPECTED ; HERE", True)
        self.idx_incr()
        return TreeSegment(None, expr, delim)
    
    def raise_stmnt(self):
        kw_raise = self.curr_tok
        self.idx_incr()
        error = self.look_for([IDENTIFIER], self.curr_tok,  "Expected Error Identifier Here", True)
        self.idx_incr()
        lparen = self.curr_tok
        value = self.expr_paren(self.expr_or)
        rparen = self.curr_tok
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "Expecting ; here", True)
        self.idx_incr()
        args = TreeSegment(lparen, value, rparen)
        stmt = TreeSegment(kw_raise, error, args)
        return TreeSegment(None, stmt, delim)

    def try_block(self):
        kw_try = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, "Expected : Here", True)
        sub_stmnt = self.code_block()
        return TreeSegment(kw_try, colon, sub_stmnt)

    def catch_block(self):    
        kw_catch = self.look_for(["KW_CATCH"], self.curr_tok, "Expected catch block Here", True)
        self.idx_incr()
        lparen = self.curr_tok
        value = self.expr_paren(self.error_atom)
        rparen = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, "Expected : Here", True)
        sub_stmnt = self.code_block()

        error_val = TreeSegment(lparen, value, rparen)
        catch_block = TreeSegment(kw_catch, error_val, colon)
        catch_block = TreeSegment(None, catch_block, sub_stmnt)
        return catch_block

    def try_stmnt(self):
        try_block = self.try_block()
        catch_block = None
        finally_block = None

        while self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()
        catch_block = self.catch_block()        
        while self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()

        if self.curr_tok == "KW_FINALLY":
            finally_block = self.try_block()
        
        return TreeSegment(try_block, catch_block, finally_block)

    def cast_expr(self):
        res = self.curr_tok
        self.idx_incr()
        return res

    def cast_stmnt(self):
        lparen = self.curr_tok
        data_type = self.expr_paren(self.cast_expr)
        rparen = self.curr_tok
        self.idx_incr()
        self.look_for([IDENTIFIER], self.curr_tok, "Expecting Identifier", True)
        iden = self.rule_iden()
        cast_type = TreeSegment(lparen, data_type, rparen)
        return TreeSegment(None, cast_type, iden)
    
    def info_stmnt(self):
        kw_info = self.curr_tok
        self.idx_incr()
        lparen = self.curr_tok
        value = self.expr_paren(self.info_atom)
        rparen = self.curr_tok
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "Expecting ; here", True)
        self.idx_incr()
        args = TreeSegment(lparen, value, rparen)
        return TreeSegment(kw_info, args, delim)

    def swap_stmnt(self):
        kw_swap = self.curr_tok
        self.idx_incr()
        lparen = self.curr_tok
        iden_list = self.expr_paren(self.swap_atom)
        rparen = self.curr_tok
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "Expected ; here", True)
        self.idx_incr()
        value = TreeSegment(lparen, iden_list, rparen)
        return TreeSegment(kw_swap, value, delim)

    def check_stmnt(self):
        kw_check = self.curr_tok
        self.idx_incr()
        lparen = self.curr_tok
        args_val = self.expr_paren(self.check_atom)
        rparen = self.curr_tok
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, "Expected ; here", True)
        self.idx_incr()
        value = TreeSegment(lparen, args_val, rparen)
        return TreeSegment(kw_check, value, delim)
#endregion