from lexer.luseed_tokens import *

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
LIT_DATA = [LIT_INT, LIT_FLT, LIT_DBL, LIT_CHAR, LIT_STR]

# LIST OF VALUES
VALUE_LIST = [LIT_INT, LIT_FLT, LIT_DBL, LIT_CHAR, LIT_STR, IDENTIFIER]

DATA_TYPE = ["KW_DATA_INT", "KW_DATA_FLT", "KW_DATA_DBL", "KW_DATA_CHAR", "KW_DATA_STR", "KW_DATA_BOOL", "KW_DATA_LIST", "KW_DATA_OBJ", "KW_DATA_CONST",]

# ACCESS MODIFIERS
ACCESS_MOD = ["KW_PUB", "KW_PRIV", "KW_PROT"]

# STATEMENTS
IMPORT_STMNT = [
                # import <IDENTIFIER>;
                [[[IDENTIFIER], 'Invalid Import statement', True], 
                [["DLM_TRMNTR"], 'Missing ;', True]],

                # from <IDENTIFIER> import (<all> | <IDENTIFIER>);
                [[[IDENTIFIER], 'Expecting an identifier', True],
                 [["KW_IMPORT"], 'Expecting keyword import', True],
                 [["KW_ALL", IDENTIFIER], 'Expecting keyword all or an Identifier', True],
                 [["DLM_TRMNTR"], 'Missing ;', True]]
               ]

MAIN_STMNT = [
                [["DLM_LPRN"], 'Expecting ( here', True],
                [["DLM_RPRN"], 'Expecting ) here', True],
                [["DLM_CODEBLK"], 'Expecting : here', True]
             ]