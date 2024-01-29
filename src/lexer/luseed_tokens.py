SPECIAL_CHAR = [".", "+", "-", "*", "/", "%", "<", ">", "=", "\\", "\"", "\'", ",", ";", "|", "!", "(", ")", "[", "]", "{", "}", "_", "^", "~", "&", ":", "?", "^", "#", "@", "-", "`"]
DOUBLE_OP = ["+", "-", "*", "/", "%", "~", "=", "!", "<", ">"]
ESCAPE_CHAR = ["n", "t", "v", "\'", "\"", "\\"]

###############################################
# TOKEN IDENTIFICATION
###############################################

# LITERALS
LIT_CHAR = "LIT_CHAR"
LIT_STR = "LIT_STR"
LIT_INT = "LIT_INT"
LIT_FLT = "LIT_FLT"
LIT_DBL = "LIT_DBL"

# COMMENTS
CMNT_SINGLE = "CMNT_SINGLE"
CMNT_MULTI = "CMNT_MULTI"

# IDENTIFIER
IDENTIFIER = "IDENTIFIER"

# UNKNOWN
UNKNOWN_TOKEN = "UNKNOWN_TOKEN"

# KEYWORD DICTIONARY
KEYWORDS = {
    # NoneType
    "null"          : "KW_NULL",

    # Input/Output Statements
    "ask"           : "KW_ASK",
    "display"       : "KW_DISPLAY",

    # Import Statements
    "import"        : "KW_IMPORT",
    "from"          : "KW_FROM",
    "all"           : "KW_ALL",

    # Conditional Statements
    "if"            : "KW_IF",
    "elif"          : "KW_ELIF",
    "else"          : "KW_ELSE",
    "then"          : "KW_THEN",
    
    # Loop statements
    "do"            : "KW_LOOP_DO",
    "for"           : "KW_LOOP_FOR",
    "foreach"       : "KW_LOOP_FOREACH",
    "repeat"        : "KW_LOOP_REPEAT",
    "until"         : "KW_LOOP_UNTIL",
    "while"         : "KW_LOOP_WHILE",
    "in"            : "KW_LOOP_IN",

    # Functions
    "main"          : "KW_MAIN",
    "func"          : "KW_FUNC",
    "return"        : "KW_RETURN",

    # Classes
    "class"         : "KW_CLASS",
    "init"          : "KW_INIT",
    "inheritall"    : "KW_INHRTALL",
    "this"          : "KW_THIS",

    # Access Modifiers
    "public"        : "KW_PUB",
    "private"       : "KW_PRIV",
    "protected"     : "KW_PROT",

    # Boolean values
    "true"          : "KW_TRUE",
    "false"         : "KW_FALSE",

    # Boolean Operators
    "and"           : "KW_BOOL_AND",
    "or"            : "KW_BOOL_OR",
    "not"           : "KW_BOOL_NOT",

    # Data type keywords
    "int"           : "KW_DATA_INT",
    "float"         : "KW_DATA_FLT",
    "double"        : "KW_DATA_DBL",
    "char"          : "KW_DATA_CHAR",
    "str"           : "KW_DATA_STR",
    "bool"          : "KW_DATA_BOOL",
    "list"          : "KW_DATA_LIST",
    "obj"           : "KW_DATA_OBJ",
    "const"         : "KW_DATA_CONST",

    # Control Statements
    "pass"          : "KW_PASS",
    "break"         : "KW_BREAK",
    "continue"      : "KW_CONTINUE",

    # Error Handling
    "try"           : "KW_TRY",
    "catch"         : "KW_CATCH",
    "finally"       : "KW_FINALLY",
    "raise"         : "KW_RAISE",

    # Documentation Statement
    "info"          : "KW_INFO",
    "quit"          : "KW_QUIT",

    # Check Functionality - New Feature
    "check"         : "KW_CHECK",

    # Swap Functionality - New Feature
    "swap"          : "KW_SWAP"
}

# NOISEWORDS
NOISEWORDS = {
    "boolean"       : "bool",
    "character"     : "char",
    "constant"      : "const",
    "integer"       : "int",
    "information"   : "info",
    "initialize"    : "init",
    "object"        : "obj",
    "string"        : "str"
}
# endregion

# OPERATORS
OP_ASSIGNMENT = {
    "="             : "OP_ASGN",
    "+="            : "OP_ADD_ASGN",
    "-="            : "OP_SUB_ASGN",
    "*="            : "OP_MUL_ASGN",
    "/="            : "OP_DIVD_ASGN",
    "%="            : "OP_MOD_ASGN",
    "~="            : "OP_FLRDIVD_ASGN"
}
# endregion

OP_ARITHMETIC = {
    "+"             : "OP_PLUS",
    "-"             : "OP_MINUS",
    "*"             : "OP_MUL",
    "/"             : "OP_DIVD",
    "%"             : "OP_MOD",
    "~"             : "OP_FLRDIVD",
    "**"            : "OP_EXPO"
}
# endregion

OP_UNARY = {
    "++"            : "OP_INCR",
    "--"            : "OP_DECR",
}
# endregion

OP_RELATION = {
    "=="            : "OP_EQ",
    "!="            : "OP_INEQ",
    ">"             : "OP_GRTR_THAN",
    "<"             : "OP_LSS_THAN",
    ">="            : "OP_GRTR_EQUAL",
    "<="            : "OP_LSS_EQUAL",
}
# endregion

# DELIMITERS
DELIMITERS = {
    ";"             : "DLM_TRMNTR",
    ":"             : "DLM_CODEBLK",
    "{"             : "DLM_LCURLY",
    "}"             : "DLM_RCURLY",
    "["             : "DLM_LSQUARE",
    "]"             : "DLM_RSQUARE",
    "("             : "DLM_LPRN",
    ")"             : "DLM_RPRN",
    ","             : "DLM_SPRTR",
    "."             : "DLM_OBJECT"
}
# endregion

# ESCAPE SEQUENCES
ESCAPE_SEQUENCES = {
    r"\n"           : "NEW_LINE",
    r"\t"           : "HORIZONTAL_TAB",
    r"\v"           : "VERTICAL_TAB",
    r"\'"           : "SINGLE_QUOTE",
    r"\""           : "DOUBLE_QUOTE",
    r"\\"           : "BACKSLASH"
}
# endregion

# WHITESPACES
WHITESPACES = {
    " "             : "WHT_SPACE",
    "\n"            : "WHT_NEWLINE"
}

WHITESPACE_REP = {
    "WHT_SPACE"    : " ",
    "WHT_NEWLINE"  : "\\n"
}
# endregion

# COMMENTS
COMMENTS = {
    "//"            : "CMNT_SINGLE", 
    "/*"            : "CMNT_MULTI_OPN", 
    "*/"            : "CMNT_MULTI_CLS"
}
# endregion
