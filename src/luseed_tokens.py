SPECIAL_CHAR = [".", "+", "-", "*", "/", "%", "<", ">", "=", "\\", "\"", "\'", ",", ";", "|", "!", "(", ")", "[", "]", "{", "}", "_", "^", "~", "&", ":", "?", "^", "#", "@", "-", "`"]
DOUBLE_OP = ["+", "-", "*", "/", "%", "~", "=", "!", "<", ">"]
ESCAPE_CHAR = ["n", "t", "v", "\'", "\"", "\\"]

###############################################
# TOKEN IDENTIFICATION
###############################################

# LITERALS
CHAR_LITERAL = "CHAR_LITERAL"
STR_LITERAL = "STR_LITERAL"
INT_LITERAL = "INT_LITERAL"
FLOAT_LITERAL = "FLOAT_LITERAL"
DOUBLE_LITERAL = "DOUBLE_LITERAL"

# COMMENTS
COMMENT_SNGLELINE = "COMMENT_SNGLELINE"
COMMENT_MLTILINE = "COMMENT_MLTILINE"

# IDENTIFIER
IDENTIFIER = "IDENTIFIER"

# UNKNOWN
UNKNOWN_TOKEN = "UNKNOWN_TOKEN"

# KEYWORD DICTIONARY
KEYWORDS = {
    # NoneType
    "null"          : "KYWRD_NULL",

    # Input/Output Statements
    "ask"           : "KYWRD_ASK",
    "display"       : "KYWRD_DISPLAY",

    # Import Statements
    "import"        : "KYWRD_IMPORT",
    "from"          : "KYWRD_FROM",
    "all"           : "KYWRD_ALL",

    # Conditional Statements
    "if"            : "KYWRD_IF",
    "elif"          : "KYWRD_ELIF",
    "else"          : "KYWRD_ELSE",
    "then"          : "KYWRD_THEN",
    
    # Loop statements
    "do"            : "KYWRD_LOOP_DO",
    "for"           : "KYWRD_LOOP_FOR",
    "foreach"       : "KYWRD_LOOP_FOREACH",
    "repeat"        : "KYWRD_LOOP_REPEAT",
    "until"         : "KYWRD_LOOP_UNTIL",
    "while"         : "KYWRD_LOOP_WHILE",
    "in"            : "KYWRD_LOOP_IN",

    # Functions
    "main"          : "KYWRD_MAIN",
    "func"          : "KYWRD_FUNC",
    "return"        : "KYWRD_RETURN",

    # Classes
    "class"         : "KYWRD_CLASS",
    "init"          : "KYWRD_INIT",
    "inheritall"    : "KYWRD_INHRTALL",
    "this"          : "KYWRD_THIS",

    # Access Modifiers
    "public"        : "KYWRD_PUBLIC",
    "private"       : "KYWRD_PRIVATE",
    "protected"     : "KYWRD_PROTECTED",

    # Boolean values
    "true"          : "KYWRD_TRUE",
    "false"         : "KYWRD_FALSE",

    # Boolean Operators
    "and"           : "KYWRD_BOOL_AND",
    "or"            : "KYWRD_BOOL_OR",
    "not"           : "KYWRD_BOOL_NOT",

    # Data type keywords
    "int"           : "KYWRD_DATA_INT",
    "float"         : "KYWRD_DATA_FLOAT",
    "double"        : "KYWRD_DATA_DOUBLE",
    "char"          : "KYWRD_DATA_CHAR",
    "str"           : "KYWRD_DATA_STR",
    "bool"          : "KYWRD_DATA_BOOL",
    "list"          : "KYWRD_DATA_LIST",
    "obj"           : "KYWRD_DATA_OBJ",
    "const"         : "KYWRD_DATA_CONST",

    # Control Statements
    "pass"          : "KYWRD_PASS",
    "break"         : "KYWRD_BREAK",
    "continue"      : "KYWRD_CONTINUE",

    # Error Handling
    "try"           : "KYWRD_TRY",
    "catch"         : "KYWRD_CATCH",
    "finally"       : "KYWRD_FINALLY",
    "raise"         : "KYWRD_RAISE",

    # Documentation Statement
    "info"          : "KYWRD_INFO",
    "quit"          : "KYWRD_QUIT",

    # Check Functionality - New Feature
    "check"         : "KYWRD_CHECK",

    # Swap Functionality - New Feature
    "swap"          : "KYWRD_SWAP"
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

# OPERATORS
OP_ASSIGNMENT = {
    "="             : "OP_ASSIGN",
    "+="            : "OP_ADD_ASSIGN",
    "-="            : "OP_SUBTRCT_ASSIGN",
    "*="            : "OP_MULTPLY_ASSIGN",
    "/="            : "OP_DIVD_ASSIGN",
    "%="            : "OP_MODULO_ASSIGN",
    "~="            : "OP_FLRDIVD_ASSIGN"
}

OP_ARITHMETIC = {
    "+"             : "OP_ADD",
    "-"             : "OP_SUBTRCT",
    "*"             : "OP_MULTPLY",
    "/"             : "OP_DIVD",
    "%"             : "OP_MODULO",
    "~"             : "OP_FLRDIVD",
    "**"            : "OP_EXPONENT"
}

OP_UNARY = {
    "+"             : "OP_POSITIVE",
    "-"             : "OP_NEGATIVE", 
    "++"            : "OP_INCREMENT",
    "--"            : "OP_DECREMENT",
}

OP_RELATION = {
    "=="            : "OP_EQUALITY",
    "!="            : "OP_INEQUALITY",
    ">"             : "OP_GREATER_THAN",
    "<"             : "OP_LESS_THAN",
    ">="            : "OP_GREATER_OR_EQUAL",
    "<="            : "OP_LESS_OR_EQUAL",
}

# DELIMITERS
DELIMITERS = {
    ";"             : "DELIM_STMT_TERMINATOR",
    ":"             : "DELIM_CODEBLK_INDICATOR",
    "{"             : "DELIM_OPEN_CURLY_BRCKT",
    "}"             : "DELIM_CLOSE_CURLY_BRCKT",
    "["             : "DELIM_OPEN_SQUARE_BRCKT",
    "]"             : "DELIM_CLOSE_SQUARE_BRCKT",
    "("             : "DELIM_OPEN_PRNTHSIS",
    ")"             : "DELIM_CLOSE_PRNTHSIS",
    ","             : "DELIM_SEPARATOR",
    "."             : "DELIM_OBJECT"
}

# ESCAPE SEQUENCES
ESCAPE_SEQUENCES = {
    r"\n"           : "NEW_LINE",
    r"\t"           : "HORIZONTAL_TAB",
    r"\v"           : "VERTICAL_TAB",
    r"\'"           : "SINGLE_QUOTE",
    r"\""           : "DOUBLE_QUOTE",
    r"\\"           : "BACKSLASH"
}

# WHITESPACES
WHITESPACES = {
    " "             : "WHT_SPACE",
    "\n"            : "WHT_NEWLINE"
}

# COMMENTS
COMMENTS = {
    "//"            : "CMMNT_SINGLE", 
    "/*"            : "CMMNT_MULTI_OPEN", 
    "*/"            : "CMMNT_MULTI_CLOSE"
}

###############################################
# TOKEN RULES
###############################################

# PRECEDENCE OF OPERATIONS (TOP TO BOTTOM)
EXPONENTIATE = ["OP_EXPONENT"]
UNARY = ["OP_POSITIVE", "OP_NEGATIVE", "OP_INCREMENT", "OP_DECREMENT", "KYWRD_BOOL_NOT"]
MULTIPLICATIVE = ["OP_MULTIPLY", "OP_MULTPLY", "OP_DIVD", "OP_MODULO", "OP_FLRDIVD"]
ADDITIVE = ["OP_ADD", "OP_SUBTRCT"]
RELATION = ["OP_GREATER_THAN", "OP_LESS_THAN", "OP_GREATER_OR_EQUAL", "OP_LESS_OR_EQUAL"]
EQUALITY = ["OP_EQUALITY", "OP_INEQUALITY"]
AND_OP = ["KYWRD_BOOL_AND"]
OR_OP = ["KYWRD_BOOL_OR"]
ASSIGNMENT = OP_ASSIGNMENT.values()

# DATA TYPES
DATA_TYPE = ["KYWRD_DATA_INT", "KYWRD_DATA_FLOAT", "KYWRD_DATA_DOUBLE", "KYWRD_DATA_CHAR", 
             "KYWRD_DATA_STR", "KYWRD_DATA_BOOL", "KYWRD_DATA_LIST", "KYWRD_DATA_OBJ", "KYWRD_DATA_CONST"]

# DATA TYPES
DATA_LIT = [INT_LITERAL, FLOAT_LITERAL, DOUBLE_LITERAL, CHAR_LITERAL, STR_LITERAL]

# DATA TYPE VARIATIONS
TEXT_DATA = [CHAR_LITERAL, STR_LITERAL]
NUM_DATA = [INT_LITERAL, FLOAT_LITERAL, DOUBLE_LITERAL]

# ACCESS MODIFIERS
ACCESS_MOD = ["KYWRD_PUBLIC", "KYWRD_PRIVATE", "KYWRD_PROTECTED"]

# BOOLEAN VALUES
BOOL_VAL = ["KYWRD_TRUE", "KYWRD_FALSE",]

# BOOL OPERATORS
OP_BOOL = ["KYWRD_BOOL_AND", "KYWRD_BOOL_OR", "KYWRD_BOOL_NOT",]
