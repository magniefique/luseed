"""
IMPORT STATEMENT
"""
# kw_from = self.curr_tok
# self.idx_incr()
# self.look_for(["IDENTIFIER"], self.curr_tok, 'Expecting an proper library/module', True)
# library = self.curr_tok
# self.idx_incr()
# self.look_for(["KW_IMPORT"], self.curr_tok, 'Expecting keyword import.', True)
# kw_import = self.curr_tok
# self.idx_incr()
# self.look_for(["IDENTIFIER", "KW_ALL"], self.curr_tok, 'Invalid import statement present', True)
# library_prop = self.curr_tok
# self.idx_incr()

# left_node = self.curr_tok
# self.idx_incr()
# self.look_for(["IDENTIFIER"], self.curr_tok, "Invalid import statement, must be an identifer", True)
# root_node = self.curr_tok
# self.idx_incr()
# self.look_for(["DLM_TRMNTR"], self.curr_tok, f"Missing ; {self.curr_tok.token, self.tk_list[self.idx_ctr-1], self.curr_tok.line}", True)
# right_node = self.curr_tok

#def expr_stmnt(self):
#     """
#     Parses an expression statement. (Ex. 3 + 5;, IDENTIFIER;)
#     """
#     res = self.expr_parse()
#     curr_tok = self.curr_tok
#     self.look_for(["DLM_TRMNTR"], self.curr_tok, f"Missing ; {self.curr_tok.token, self.tk_list[self.idx_ctr-1], self.curr_tok.line}", True)
#     self.idx_incr() 
#     return TreeSegment(None, res, curr_tok)

# elif self.curr_tok.token == "DLM_LPRN" and is_dec:
        #     raise Exception("Function call cannot be a declaration statement")

        # elif self.curr_tok.token == "DLM_TRMNTR" and is_dec:
        #     curr_stmnt = TreeSegment(None, identifier, self.curr_tok.token)
        #     self.idx_incr()