from lexer.luseed_tokens import *
from luseed_error import *

# PRECEDENCE OF OPERATIONS (HIGHER TO LOWER)
EXPR_EXPO   = ["OP_EXPO"]
EXPR_UN     = ["OP_POS", "OP_NEG", "KW_BOOL_NOT"]
EXPR_MUL    = ["OP_MULTIPLY", "OP_MUL", "OP_DIVD", "OP_MOD", "OP_FLRDIVD"]
EXPR_ADD    = ["OP_PLUS", "OP_MINUS"]
EXPR_REL    = ["OP_GRTR_THAN", "OP_LSS_THAN", "OP_GRTR_EQUAL", "OP_LSS_EQUAL"]
EXPR_EQ     = ["OP_EQ", "OP_INEQ"]
EXPR_AND    = ["KW_BOOL_AND"]
EXPR_OR     = ["KW_BOOL_OR"]

# DATA LITERALS FOR ATOMS 
LIT_DATA = [LIT_INT, LIT_FLT, LIT_DBL, LIT_CHAR, LIT_STR, LIT_BOOL_TRUE, LIT_BOOL_FALSE]

# LIST OF VALUES
VALUE_LIST = [LIT_INT, LIT_FLT, LIT_DBL, LIT_CHAR, LIT_STR, LIT_BOOL_TRUE, LIT_BOOL_FALSE, IDENTIFIER]

DATA_TYPE = ["KW_DATA_INT", "KW_DATA_FLT", "KW_DATA_DBL", "KW_DATA_CHAR", "KW_DATA_STR", "KW_DATA_BOOL", "KW_DATA_LIST", "KW_DATA_OBJ", "KW_DATA_CONST",]

# ACCESS MODIFIERS
ACCESS_MOD = ["KW_PUB", "KW_PRIV", "KW_PROT"]

# STATEMENT MAP (FOR LENGTHY REPETITIVE STATEMENTS)
IMPORT_STMNT = [
                # import <IDENTIFIER>;
                [[[IDENTIFIER], Error.SyntaxError.INVALID_IMPORT, True], 
                 [["DLM_TRMNTR"], Error.SyntaxError.EXPECTING_SEMICOLON, True]],

                # from <IDENTIFIER> import (<all> | <IDENTIFIER>);
                [[[IDENTIFIER], Error.SyntaxError.EXPECTING_IDEN, True],
                 [["KW_IMPORT"], Error.SyntaxError.IMPORT_ERROR, True],
                 [["KW_ALL", IDENTIFIER], Error.SyntaxError.IMPORT_IDEN_ERROR, True],
                 [["DLM_TRMNTR"], Error.SyntaxError.EXPECTING_SEMICOLON, True]]
               ]

MAIN_STMNT = [
                [["DLM_LPRN"], Error.SyntaxError.EXPECTING_LPAREN, True],
                [["DLM_RPRN"], Error.SyntaxError.EXPECTING_RPAREN, True],
                [["DLM_CODEBLK"], Error.SyntaxError.EXPECTING_COLON, True]
             ]