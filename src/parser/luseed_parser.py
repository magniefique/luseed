from lexer.luseed_token import *
from luseed_error import *
from parser.grammar import *
import time

class TreeSegment:
    """
    Segment of the tree that contains the root node, the left node, and the right node (Originally applied for the Operator Precedence)
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
    def __init__(self, list: list):
        self.tk_list = list[0]
        self.line_list = list[1]
        self.idx_ctr = -1
        self.is_done = False
        self.debugger = 0
        self.idx_incr()
    
    def idx_incr(self):
        self.idx_ctr += 1
        if self.idx_ctr < len(self.tk_list):
            self.curr_tok = self.tk_list[self.idx_ctr]
            self.look_for(["UNKNOWN_TOKEN"], self.curr_tok, Error.SyntaxError.UNKNOWN_TOKEN + self.curr_tok.line, False)
            
        else:
            self.is_done = True
            self.curr_tok = Token(self.curr_tok.line, " ",  "EOF")
            return

        return self.curr_tok

    def idx_dcr(self):
        """
        Decrements the index counter and sets the current token to the previous token.
        """
        self.idx_ctr -= 1

        self.curr_tok = self.tk_list[self.idx_ctr]
        return self.curr_tok

    def look_for(self, token: list, tok: Token, error: str, accept: bool):
        """
        Checks if the current token satisfies the specified token. If this is True, accept the given specified token, and not if False.
        """
        if (accept and tok.token in token) or (not accept and tok.token not in token):
            return tok
        
        self.parse_error(error, tok)

    def parse(self):
        """
        Starts the parsing process.
        """
        init_time = time.time()
        while not self.is_done:
            parse_res = self.stmnt()
            print(parse_res)
        final_time = time.time()
        elapsed_time = final_time - init_time

        print(f"\nSuccessful Parse!\nElapsed Parsing Time\t: {elapsed_time}")

    def parse_error(self, error: str, token: Token):
        """
        Handles the parser errors.
        """
        Error.SyntaxError(error, token, self.line_list).displayerror()

    def expr_parse(self):
        """
        Parses an expression. This is used mainly for assignment statements.
        """
        res = self.expr_or()
        
        self.look_for(OP_ASSIGNMENT.values(), self.curr_tok, Error.SyntaxError.INVALID_ASSIGN, False)
        self.look_for(["DLM_RPRN"], self.curr_tok, Error.SyntaxError.INVALID_PAREN, False)
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
        Values that can be used in an expression.  
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
                res = self.expr_paren(self.atom_paren, True)
                self.idx_incr()

            return res
        
        # Used for lists
        elif curr_tok.token == "DLM_LSQUARE":
            self.idx_incr()
            lsquare = curr_tok
            list_val = self.args_list()
            rsquare = self.look_for(["DLM_RSQUARE"], self.curr_tok, Error.SyntaxError.EXPECTING_RSQUARE + self.curr_tok.line, True)
            self.idx_incr()
            return TreeSegment(lsquare, list_val, rsquare)

        # Used for unary operators
        elif self.curr_tok.token in ["OP_PLUS", "OP_MINUS", "KW_BOOL_NOT"]:
            if self.curr_tok.token == "OP_PLUS":
                self.curr_tok.token = "OP_POS"
            
            elif self.curr_tok.token == "OP_MINUS":
                self.curr_tok.token = "OP_NEG"

            return None
        
        elif curr_tok.token == "KW_ASK":
            return self.io_expr(curr_tok)

        elif curr_tok.token in ["DLM_RPRN", "DLM_TRMNTR"]:
            self.parse_error(Error.SyntaxError.EXPECTING_OPERAND, curr_tok)
        
        else:
            self.parse_error(Error.SyntaxError.INVALID_VALUE, curr_tok)

    def atom_paren(self):
        """
        Contains the contents of a equation within a parenthesis which cannot be empty
        """
        self.look_for(["DLM_RPRN"], self.curr_tok, Error.SyntaxError.INVALID_EXPR_PAREN, False)#### CANNOT BE EMPTY EX. () + 3
        return self.expr_or()

    def expr_paren(self, func, is_op: bool = False):
        """
        Function that handles different parenthetical expressions
        """
        lparen = self.look_for(["DLM_LPRN"], self.curr_tok, Error.SyntaxError.EXPECTING_LPAREN + self.curr_tok.line, True)############
        self.idx_incr()
        res = func()
        rparen = self.look_for(["DLM_RPRN"], self.curr_tok, Error.SyntaxError.EXPECTING_RPAREN + self.curr_tok.line, True)################################ CANNOT BE MISSING A RIGHT PARENTHESIS
        
        return res if is_op else TreeSegment(lparen, res, rparen)

    def expr_operation(self, func, acc_op: list, assoc: str): 
        """
        Recursion Function for Operator Precedence
        """
        left_node = func()
        if self.curr_tok.token in ["DLM_TRMNTR", "WHT_NEWLINE"]:
            return left_node
        
        # ERROR VALUES FOR PARENTHESIS AND VALUE LIST
        self.look_for(VALUE_LIST, self.curr_tok, Error.SyntaxError.EXPECTING_OP + self.curr_tok.line, False) #########CHECKS FOR THE NEXT OPERATOR ERROR IF: 3 3 + 3, IDEN IDEN * IDEN

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

    def rule_iden(self, is_idenstmnt: bool = False):
        """
        Rules for Identifiers.
        """
        iden_tok = self.curr_tok
        self.idx_incr()

        if iden_tok.token == "KW_THIS":
            self.look_for(["DLM_OBJECT"], self.curr_tok, Error.SyntaxError.THIS_ERROR, True)

        if self.curr_tok.token == "DLM_OBJECT":
            left_node = iden_tok
            
            while self.curr_tok.token == "DLM_OBJECT":
                self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, False)
                root_node = self.curr_tok
                right_node = self.obj_atom()
                left_node = TreeSegment(left_node, root_node, right_node)
            
            return left_node

        elif self.curr_tok.token == "DLM_LSQUARE":
            res = self.list_idx()
            return TreeSegment(None, iden_tok, res)

        elif self.curr_tok.token == "DLM_LPRN" and not is_idenstmnt:
            iden_tok = self.call_expr(iden_tok)

        return iden_tok

    def list_idx(self):
        """
        List Index for Identifiers. Ex. testList[1] <- list_idx.
        """
        lsquare = self.curr_tok
        self.idx_incr()
        if self.curr_tok.token in VALUE_LIST or self.curr_tok.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_BOOL_NOT"]:
            idx_value = self.expr_or()
        
        else:
            self.parse_error(Error.SyntaxError.INVALID_VALUE, self.curr_tok)

        rsquare = self.look_for(["DLM_RSQUARE"],  self.curr_tok, Error.SyntaxError.EXPECTING_RSQUARE + self.curr_tok.line, True)
        self.idx_incr()
        if self.curr_tok.token == "DLM_LSQUARE":
            res = TreeSegment(lsquare, idx_value, rsquare)
            next_idx = self.list_idx()
            res = TreeSegment(None, res, next_idx)
            return res
        
        return TreeSegment(lsquare, idx_value, rsquare)

    def args_list(self):
        """
        List of arguments that is passed in a method call/function call/class instantiation.
        """
        arg_list = self.curr_tok
        if arg_list.token in VALUE_LIST or arg_list.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_BOOL_NOT", "KW_THIS"]:
            return self.expr_operation(self.args_atom, ['DLM_SPRTR'], 'L')

        elif arg_list.token in ["DLM_RPRN", "DLM_RSQUARE"]:
            return None

        else:
            self.parse_error(Error.SyntaxError.INVALID_VALUE, arg_list)

    def args_atom(self):
        """
        Accepted values that can be passed as arguments.
        """
        self.look_for(["DLM_RPRN"], self.curr_tok, Error.SyntaxError.EXPECTING_VAL + self.curr_tok.line, False)
        res = self.expr_or()
        return res

    def dec_atom(self):
        """
        Accepted values in a declaration statement.
        """
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
            self.parse_error(Error.SyntaxError.EXPECTING_DEC + self.curr_tok.line, self.curr_tok)
    
    def param_list(self):
        """
        List of parameters.
        """
        return self.expr_operation(self.param_atom, ["DLM_SPRTR"], 'L')

    def param_atom(self):
        """
        List of each atom that can be present in a parameter. Ex. int a, char b = 'a'.
        """
        if self.curr_tok.token in DATA_TYPE:
            dataType = self.curr_tok
            self.idx_incr()
            identifier = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
            self.idx_incr()
            return  TreeSegment(None, dataType, identifier)
        
        elif self.curr_tok.token == "KW_THIS":
            kw_this = self.curr_tok
            self.idx_incr()
            return kw_this
        
        elif self.curr_tok.token == "DLM_RPRN":
            return None

        else:
            self.parse_error(Error.SyntaxError.INVALID_VALUE, self.curr_tok)

    def obj_atom(self):
        """
        Atom that can be used as a property. Ex. TestClass.test <- obj_atom
        """
        self.idx_incr()
        self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        return self.rule_iden()
    
    def info_atom(self):
        """
        Atoms for the info statement.
        """
        if self.curr_tok.token in VALUE_LIST or self.curr_tok.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_BOOL_NOT"]:
            return self.expr_or()
        
        elif self.curr_tok.token in KEYWORDS.values():
            res = self.curr_tok
            self.idx_incr()
            return res

    def swap_atom(self):
        """
        Atoms for the swap statement. Can be either 2 or 3 identifiers only.
        """
        atom_1 = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        sep_1 = self.look_for(["DLM_SPRTR"], self.curr_tok,  Error.SyntaxError.EXPECTING_SEP + self.curr_tok.line, True)
        self.idx_incr()
        atom_2 = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        if self.curr_tok.token == "DLM_SPRTR":
            sep_2 = self.curr_tok
            self.idx_incr()
            atom_3 = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
            self.idx_incr()
            return f'{atom_1}, {sep_1}, {atom_2}, {sep_2}, {atom_3}'
        
        elif self.curr_tok.token == "DLM_RPRN":
            return f'{atom_1}, {sep_1}, {atom_2}'

    def check_atom(self):
        """
        Atoms for the check function.
        """
        self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        iden = self.rule_iden()

        return iden

    def for_expr(self):
        """
        The expression for the for loop. This includes the initialization, condition, and update of the for loop.
        """
        if self.curr_tok.token in DATA_TYPE:
            data_type = self.curr_tok
            self.idx_incr()
        else:
            data_type = None

        iden = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        self.look_for(OP_ASSIGNMENT.values(), self.curr_tok, Error.SyntaxError.EXPECTING_ASSIGN + self.curr_tok.line, True)
        init = self.assign_stmnt(iden)
        if self.curr_tok.token in VALUE_LIST or self.curr_tok.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_BOOL_NOT"]:
            expr = self.expr_parse()

        else:
            self.parse_error(Error.SyntaxError.INVALID_VALUE, self.curr_tok)

        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
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
                self.parse_error(Error.SyntaxError.EXPECTING_UN, self.curr_tok)

        else:
            self.parse_error(Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, self.curr_tok)

        condn = TreeSegment(None, expr, delim)
        init = TreeSegment(None, data_type, init)
        return TreeSegment(init, condn, update)

    def foreach_expr(self):
        """
        Contains the arguments for a foreach loop.
        """
        data_type = self.look_for(DATA_TYPE, self.curr_tok, Error.SyntaxError.EXPECTING_DATA_TYPE + self.curr_tok.line, True)
        self.idx_incr()
        iden = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        kw_in = self.look_for(["KW_LOOP_IN"], self.curr_tok, Error.SyntaxError.IN_ERROR, True)
        self.idx_incr()
        list_var = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        dec = TreeSegment(None, data_type, iden)
        return TreeSegment (dec, kw_in, list_var)

    def error_atom(self):
        """
        Possible values that can be and error. This is an identifier since Errors are Classes in python which is where is this based.
        """
        error = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        return error

    def code_block(self, is_loop = False):
        """
        The code block for complex statements.
        """
        self.idx_incr()
        if self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()

        lcurly = self.look_for(["DLM_LCURLY"], self.curr_tok,  Error.SyntaxError.EXPECTING__LCURLY + self.curr_tok.line, True)
        self.idx_incr()
        while self.curr_tok.token != "DLM_RCURLY" and not self.is_done:
            sub_stmnt = self.stmnt(is_loop)

        rcurly = self.look_for(["DLM_RCURLY"], self.curr_tok,  Error.SyntaxError.EXPECTING__RCURLY + self.curr_tok.line, True)
        self.idx_incr()

        return TreeSegment(lcurly, sub_stmnt, rcurly)

    def check_order(self, order_array):
        """
        Checks the order for the main function and the import statements.
        """
        stmnt_list = []
        stmnt_order = order_array

        for i in stmnt_order:
            self.idx_incr()
            self.look_for(i[0], self.curr_tok, i[1] + self.curr_tok.line, i[2])
            stmnt_list.append(self.curr_tok)
        
        return stmnt_list

#region Statements
    def stmnt(self, is_loop: bool=False):
        """
        Collection of all possible statements in the luseed programming language.
        """

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
            if self.curr_tok.token == "KW_DATA_CONST":
                const = self.curr_tok
                self.idx_incr()
                self.look_for(DATA_TYPE, self.curr_tok, Error.SyntaxError.EXPECTING_DATA_TYPE, True)
            
            else:
                const = None

            curr_stmnt = self.dec_stmnt()
            curr_stmnt = TreeSegment(None, const, curr_stmnt)

        elif self.curr_tok.token in ["KW_DISPLAY", "KW_ASK"]:
            curr_stmnt = self.io_stmnt()
        
        elif self.curr_tok.token == "KW_IF":
            curr_stmnt = self.if_stmnt()

        elif self.curr_tok.token == "KW_PASS":
            curr_stmnt =  self.pass_stmnt()
        
        elif self.curr_tok.token == "KW_RETURN":
            curr_stmnt = self.return_stmnt()

        elif self.curr_tok.token in ["KW_BREAK",  "KW_CONTINUE"] and is_loop:
            curr_stmnt = self.ctrl_stmnt()

        elif self.curr_tok.token in OP_UNARY.values():
            curr_stmnt = self.unary_stmnt(None, 0)

        elif self.curr_tok.token == "KW_FUNC":
            curr_stmnt = self.func_stmnt()

        elif self.curr_tok.token == "KW_LOOP_FOR":
            curr_stmnt = self.for_stmnt()

        elif self.curr_tok.token == "KW_LOOP_FOREACH":
            curr_stmnt = self.foreach_stmnt()

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
        
        elif self.curr_tok.token == "KW_LOOP":
            loop_header = self.loop_name()
            
            if self.curr_tok.token == "KW_LOOP_FOR":
                curr_stmnt = self.for_stmnt()

            elif self.curr_tok.token == "KW_LOOP_WHILE":
                curr_stmnt = self.while_stmnt()

            elif self.curr_tok.token == "KW_LOOP_DO":
                curr_stmnt = self.do_stmnt()

            elif self.curr_tok.token == "KW_LOOP_REPEAT":
                curr_stmnt = self.repeat_stmnt()

            else:
                self.parse_error(Error.SyntaxError.EXPECTING_LOOP, self.curr_tok)

            curr_stmnt = TreeSegment(None, loop_header, curr_stmnt)

        elif self.curr_tok.token == "KW_CHECK":
            curr_stmnt = self.check_stmnt()

        elif self.curr_tok.token in ACCESS_MOD:
            modifier = self.curr_tok
            self.idx_incr()
            if self.curr_tok.token in DATA_TYPE:
                if self.curr_tok.token == "KW_DATA_CONST":
                    const = self.curr_tok
                    self.idx_incr()
                    self.look_for(DATA_TYPE, self.curr_tok, Error.SyntaxError.EXPECTING_DATA_TYPE, True)
            
                else:
                    const = None

                curr_stmnt = self.dec_stmnt()
                curr_stmnt = TreeSegment(None, const, curr_stmnt)
                curr_stmnt = TreeSegment(None, modifier, curr_stmnt)
            
            elif self.curr_tok.token == "KW_FUNC":
                curr_stmnt = self.func_stmnt()
                curr_stmnt = TreeSegment(None, modifier, curr_stmnt)

            elif self.curr_tok.token == "KW_CLASS":
                curr_stmnt = self.class_stmnt()
                curr_stmnt = TreeSegment(None, modifier, curr_stmnt)
            
            else:
                self.parse_error(Error.SyntaxError.EXPECTING_ACCESS_MOD + self.curr_tok.line, self.curr_tok)

            curr_stmnt = TreeSegment(None, modifier, curr_stmnt)

        elif self.curr_tok.token == "KW_ELIF":
            self.parse_error(Error.SyntaxError.ELIF_ERROR, self.curr_tok)

        elif self.curr_tok.token == "KW_ELSE":
            self.parse_error(Error.SyntaxError.ELSE_ERROR, self.curr_tok)

        elif self.curr_tok.token == "KW_CATCH":
            self.parse_error(Error.SyntaxError.CATCH_ERROR, self.curr_tok)

        elif self.curr_tok.token == "KW_FINALLY":
            self.parse_error(Error.SyntaxError.FINALLY_ERROR, self.curr_tok)

        elif self.curr_tok.token in LIT_DATA:
            self.parse_error(Error.SyntaxError.EXPRESSION_STMNT, self.curr_tok)

        else:
            self.parse_error(Error.SyntaxError.INVALID_STMNT + self.curr_tok.lexeme, self.curr_tok)

        if self.curr_tok.token != "DLM_RCURLY" and self.curr_tok.token != 'EOF':
            next_stmnt = self.stmnt(is_loop)
        
        else:
            next_stmnt = None
        
        res = TreeSegment(None, curr_stmnt, next_stmnt)
        return res

    def iden_stmnt(self):
        """
        Contains all the possible statements that can be used when an identifier is found first.
        """
        identifier = self.rule_iden(True)
        if self.curr_tok.token in OP_ASSIGNMENT.values():
            curr_stmnt = self.assign_stmnt(identifier)

        elif self.curr_tok.token == "DLM_LPRN":
            curr_stmnt = self.call_stmnt(identifier)

        elif self.curr_tok.token in OP_UNARY.values():
            curr_stmnt = self.unary_stmnt(identifier, 1)

        elif self.curr_tok.token == "DLM_TRMNTR":
            self.parse_error(Error.SyntaxError.EXPRESSION_STMNT, self.curr_tok)
        
        else:
            self.parse_error(Error.SyntaxError.EXPECTING_IDEN_STMNT + self.curr_tok.line, self.curr_tok)

        return curr_stmnt  
    
    def call_expr(self, identifier):
        """
        This is for call statements such as function calls and method calls.
        """
        args = self.expr_paren(self.args_list)
        self.idx_incr()
        return TreeSegment(None, identifier, args)

    def call_stmnt(self, identifer):
        """
        This is for call statments.
        """
        stmnt = self.call_expr(identifer)
        self.look_for(OP_ASSIGNMENT.values(), self.curr_tok, Error.SyntaxError.INVALID_ASSIGN, False)
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(None, stmnt, delim)

    def imprt_stmnt(self):
        """
        Parses the import statements.
        """
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
        """
        Parses the declaration statement of luseed.
        """
        data_type = self.curr_tok
        self.idx_incr()
        self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        res = self.expr_operation(self.dec_atom, ["DLM_SPRTR"], 'L')
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(data_type, res, delim)

    def io_expr(self, keyword):
        """
        Parses the input expressions. This is also used by assignment statements.
        """
        kw_disp = keyword
        self.idx_incr()
        args = self.expr_paren(self.args_list)
        self.idx_incr()
        return TreeSegment(None, kw_disp, args)

    def io_stmnt(self):
        """
        Parses the ask and display functions of the language.
        """
        kw_disp = self.curr_tok
        expr = self.io_expr(kw_disp)
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(None, expr, delim)
    
    def assign_expr(self, dest_value, is_assign: bool = True):
        """
        Parses the assignment expressions. This is used by for loops and assignment statements
        """
        op = self.curr_tok
        self.idx_incr()
        self.look_for(["DLM_TRMNTR", "WHT_NEWLINE"], self.curr_tok, Error.SyntaxError.EXPECTING_VAL + self.curr_tok.line, False)
        value = self.expr_parse() if is_assign else self.expr_or()
        return TreeSegment(dest_value, op, value)

    def assign_stmnt(self, dest_value):
        """
        Parses the assignment statements.
        """
        expr = self.assign_expr(dest_value)
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment (None, expr, delim)

    def func_stmnt(self):
        """
        Parses the function statements
        """
        kw_func = self.curr_tok
        self.idx_incr()
        iden = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        param = self.expr_paren(self.param_list)
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        sub_stmnt = self.code_block()
        header = TreeSegment(iden, param, colon)
        return TreeSegment(kw_func, header, sub_stmnt)
    
    def condn_block(self, with_condn: bool = True):
        """
        Condition blocks for if/else statements.
        """
        kw_start = self.curr_tok
        self.idx_incr()
        if with_condn:
            condn_expr = self.expr_paren(self.atom_paren)
            self.idx_incr()
            kw_then = self.look_for(["KW_THEN"], self.curr_tok, Error.SyntaxError.EXPECTING_THEN, True)
            self.idx_incr()

        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        sub_stmnt = self.code_block()
        # For if/elif statements
        if with_condn:
            inc_header = TreeSegment(kw_start, condn_expr, kw_then)
            condn_stmnt = TreeSegment(inc_header, colon, sub_stmnt)

        # For else statements
        else:
            condn_stmnt = TreeSegment(kw_start, colon, sub_stmnt)

        return condn_stmnt

    def if_stmnt(self):
        """
        Parses the conditional statements.
        """
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
        """
        The elif block of the if else statement.
        """
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
        """
        Parses the for loop statement.
        """
        kw_for = self.curr_tok
        self.idx_incr()
        args = self.expr_paren(self.for_expr)
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        loop_body = self.code_block(True)

        header = TreeSegment(kw_for, args, colon)
        return TreeSegment(None, header, loop_body)

    def foreach_stmnt(self):
        """
        Parses the foreach loop statement.
        """
        kw_foreach = self.curr_tok
        self.idx_incr()
        args = self.expr_paren(self.foreach_expr)
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        loop_body = self.code_block(True)

        header = TreeSegment(kw_foreach, args, colon)
        return TreeSegment(None, header, loop_body)

    def while_stmnt(self):
        """
        Parses the while loop statement.
        """
        kw_while = self.curr_tok
        self.idx_incr()
        condn = self.expr_paren(self.atom_paren)
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        loop_body = self.code_block(True)
        header = TreeSegment(kw_while, condn, colon)
        return TreeSegment(None, header, loop_body)

    def do_stmnt(self):
        """
        Parses the do-until loop statement.
        """
        kw_do = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        loop_body = self.code_block(True)
        if self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()
        kw_until = self.look_for(["KW_LOOP_UNTIL"], self.curr_tok, Error.SyntaxError.EXPECTING_UNTIL, True)
        self.idx_incr()
        condn = self.expr_paren(self.atom_paren)
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        header = TreeSegment(None, kw_do, colon)
        footer = TreeSegment(kw_until, condn, delim)
        return TreeSegment(header, loop_body, footer)

    def repeat_stmnt(self):
        """
        Parses the repeat statement.
        """
        kw_repeat = self.curr_tok
        self.idx_incr()
        args = self.expr_paren(self.args_atom)
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        loop_body = self.code_block(True)
        header = TreeSegment(kw_repeat, args, colon)
        return TreeSegment(None, header, loop_body)

    def class_stmnt(self):
        """
        Parses the class statement.
        """
        kw_class = self.curr_tok
        parent = None
        self.idx_incr()
        iden = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        if self.curr_tok.token == "DLM_LPRN":
            parent = self.expr_paren(self.rule_iden)
            self.idx_incr()
        
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        class_body = self.code_block(False)
        class_name = TreeSegment(iden, parent, colon)
        return TreeSegment(kw_class, class_name, class_body)

    def init_stmnt(self):
        """
        Parses the initialize statement in a class.
        """
        kw_init = self.curr_tok
        self.idx_incr()
        param_list = self.expr_paren(self.param_list)
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        sub_stmnt = self.code_block()
        header = TreeSegment(kw_init, param_list, colon)
        return TreeSegment(None, header, sub_stmnt)

    def pass_stmnt(self):
        """
        Parses the pass statement.
        """
        kw_pass = self.curr_tok
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return  TreeSegment(None, kw_pass, delim)
    
    def return_stmnt(self):
        kw_return = self.curr_tok
        self.idx_incr()
        if self.curr_tok.token == "DLM_TRMNTR":
            ret_val = None

        elif self.curr_tok.token in VALUE_LIST or self.curr_tok.token in ["DLM_LPRN", "DLM_LSQUARE", "KW_BOOL_NOT"]:
            ret_val = self.expr_parse()

        else:
            self.parse_error(Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, self.curr_tok)

        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(kw_return, ret_val, delim)

    def ctrl_stmnt(self):
        """
        Parses the pass statement.
        """
        kw = self.curr_tok
        self.idx_incr()
        if self.curr_tok.token == "DLM_TRMNTR":
            loop_name = None

        elif self.curr_tok.token == IDENTIFIER:
            loop_name = self.curr_tok
            self.idx_incr()

        else:
            self.parse_error(Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, self.curr_tok)

        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(kw, loop_name, delim)

    def unary_expr(self, iden_value, un_type: int):
        """
        Parses the unary expressions.
        """
        if un_type == 0:
            unary_op = self.curr_tok
            self.idx_incr()
            iden = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
            self.idx_incr()
            return TreeSegment(None, unary_op, iden)

        elif un_type == 1:
            iden = iden_value
            unary_op = self.look_for(OP_UNARY.values(), self.curr_tok, Error.SyntaxError.EXPECTING_UN + self.curr_tok.line, True)
            self.idx_incr()
            return TreeSegment(None, iden, unary_op)

    def unary_stmnt(self, iden_value = None, un_type: int = None):
        """
        Parses the unary statements.
        """
        expr = self.unary_expr(iden_value, un_type)
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(None, expr, delim)
    
    def raise_stmnt(self):
        """
        Parses the raise statement.
        """
        kw_raise = self.curr_tok
        self.idx_incr()
        error = self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_ERROR + self.curr_tok.line, True)
        self.idx_incr()
        args = self.expr_paren(self.expr_or)
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        stmt = TreeSegment(kw_raise, error, args)
        return TreeSegment(None, stmt, delim)

    def try_block(self):
        """
        Parses both the try block and the finally block of a try...catch statement.
        """
        kw_try = self.curr_tok
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        sub_stmnt = self.code_block()
        return TreeSegment(kw_try, colon, sub_stmnt)

    def catch_block(self): 
        """
        Parses the catch block of a try...catch statement.
        """   
        kw_catch = self.look_for(["KW_CATCH"], self.curr_tok, Error.SyntaxError.EXPECTING_CATCH, True)
        self.idx_incr()
        error_val = self.expr_paren(self.error_atom)
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        sub_stmnt = self.code_block()

        catch_block = TreeSegment(kw_catch, error_val, colon)
        catch_block = TreeSegment(None, catch_block, sub_stmnt)
        return catch_block

    def try_stmnt(self):
        """
        Parses the try...catch statement.
        """
        try_block = self.try_block()
        catch_block = None
        finally_block = None

        while self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()
        catch_block = self.catch_block()        
        while self.curr_tok.token == "WHT_NEWLINE":
            self.idx_incr()
        
        if self.curr_tok.token == "KW_FINALLY":
            finally_block = self.try_block()
        
        return TreeSegment(try_block, catch_block, finally_block)

    def cast_expr(self):
        """
        Used by cast stmnts. 
        """
        res = self.curr_tok
        self.idx_incr()
        return res

    def cast_stmnt(self):
        """
        Parses the cast statements
        """
        cast_type = self.expr_paren(self.cast_expr)
        self.idx_incr()
        self.look_for([IDENTIFIER], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        iden = self.rule_iden()
        return TreeSegment(None, cast_type, iden)
    
    def loop_name(self):
        """
        Handles the loop naming.
        """
        kw_loop = self.curr_tok
        self.idx_incr()
        iden = self.look_for(["IDENTIFIER"], self.curr_tok, Error.SyntaxError.EXPECTING_IDEN + self.curr_tok.line, True)
        self.idx_incr()
        colon = self.look_for(["DLM_CODEBLK"], self.curr_tok, Error.SyntaxError.EXPECTING_COLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(kw_loop, iden, colon)

    def info_stmnt(self):
        """
        Parses the info statement.
        """
        kw_info = self.curr_tok
        self.idx_incr()
        args = self.expr_paren(self.info_atom)
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(kw_info, args, delim)

    def swap_stmnt(self):
        """
        Parses the swap statement.
        """
        kw_swap = self.curr_tok
        self.idx_incr()
        iden_list = self.expr_paren(self.swap_atom)
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(kw_swap, iden_list, delim)

    def check_stmnt(self):
        """
        Parses the check statement.
        """
        kw_check = self.curr_tok
        self.idx_incr()
        args_val = self.expr_paren(self.check_atom)
        self.idx_incr()
        delim = self.look_for(["DLM_TRMNTR"], self.curr_tok, Error.SyntaxError.EXPECTING_SEMICOLON + self.curr_tok.line, True)
        self.idx_incr()
        return TreeSegment(kw_check, args_val, delim)
#endregion