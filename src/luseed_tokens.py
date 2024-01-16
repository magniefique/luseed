SPECIAL_CHAR = [".", "+", "-", "*", "/", "%", "<", ">", "=", "\\", "\"", "\'", ",", ";", "|", "!", "(", ")", "[", "]", "{", "}", "_", "^", "~", "&", ":", "?", "^", "#", "@", "-", "`"]
DOUBLE_OP = ["+", "-", "*", "/", "%", "~", "=", "!", "<", ">"]
ESCAPE_CHAR = ["n", "t", "v", "\'", "\"", "\\"]

# KEYWORD DICTIONARY
KEYWORDS = {
    "all" : "KEYWORD_ALL",
    "and" : "KEYWORD_AND",
    "ask" : "KEYWORD_ASK",
    "bool" : "KEYWORD_BOOL",
    "break" : "KEYWORD_BREAK",
    "catch" : "KEYWORD_CATCH",
    "char" : "KEYWORD_CHAR",
    "check" : "KEYWORD_CHECK",
    "class" : "KEYWORD_CLASS",
    "const" : "KEYWORD_CONST",
    "continue" : "KEYWORD_CONTINUE",
    "display" : "KEYWORD_DISPLAY",
    "do" : "KEYWORD_DO",
    "double" : "KEYWORD_DOUBLE",
    "elif" : "KEYWORD_ELIF",
    "else" : "KEYWORD_ELSE",
    "false" : "KEYWORD_FALSE",
    "finally" : "KEYWORD_FINALLY",
    "float" : "KEYWORD_FLOAT",
    "for" : "KEYWORD_FOR",
    "foreach" : "KEYWORD_FOREACH",
    "from" : "KEYWORD_FROM",
    "func" : "KEYWORD_FUNC",
    "help" : "KEYWORD_HELP",
    "if" : "KEYWORD_IF",
    "import" : "KEYWORD_IMPORT",
    "info" : "KEYWORD_INFO",
    "init" : "KEYWORD_INIT",
    "inheritall" : "KEYWORD_INHERITALL",
    "in" : "KEYWORD_IN",
    "int" : "KEYWORD_INT",
    "list" : "KEYWORD_LIST",
    "main" : "KEYWORD_MAIN",
    "not" : "KEYWORD_NOT",
    "null" : "KEYWORD_NULL",
    "obj" : "KEYWORD_OBJ",
    "or" : "KEYWORD_OR",
    "pass" : "KEYWORD_PASS",
    "private" : "KEYWORD_PRIVATE",
    "protected" : "KEYWORD_PROTECTED",
    "public" : "KEYWORD_PUBLIC",
    "quit" : "KEYWORD_QUIT",
    "raise" : "KEYWORD_RAISE",
    "repeat" : "KEYWORD_REPEAT",
    "return" : "KEYWORD_RETURN",
    "str" : "KEYWORD_STR",
    "then" : "KEYWORD_THEN",
    "this" : "KEYWORD_THIS",
    "true" : "KEYWORD_TRUE",
    "try" : "KEYWORD_TRY",
    "until" : "KEYWORD_UNTIL",
    "while" : "KEYWORD_WHILE"
}

# NOISEWORDS
NOISEWORDS = {
    "boolean" : "bool",
    "character" : "char",
    "constant" : "const",
    "integer" : "int",
    "information" : "info",
    "initialize" : "init",
    "object" : "obj",
    "string" : "str"
}

# OPERATORS
OP_ASSIGNMENT = {
    "=" : "OP_ASSIGNMENT",
    "+=" : "OP_ADDITION_ASSIGNMENT",
    "-=" : "OP_SUBTRACTION_ASSIGNMENT",
    "*=" : "OP_MULTIPLICATION_ASSIGNMENT",
    "/=" : "OP_DIVISION_ASSIGNMENT",
    "%=" : "OP_MODULO_ASSIGNMENT",
    "~=" : "OP_FLRDIVISION_ASSIGNMENT"
}

OP_ARITHMETIC = {
    "+" : "OP_ADDITION",
    "-" : "OP_SUBTRACTION",
    "*" : "OP_MULTIPLICATION",
    "/" : "OP_DIVISION",
    "%" : "OP_MODULO",
    "~" : "OP_FLRDIVISION",
    "**" : "OP_EXPONENTIATE"
}

OP_UNARY = {
    "+" : "OP_POSITIVE",
    "-" : "OP_NEGATIVE", 
    "++" : "OP_INCREMENT",
    "--" : "OP_DECREMENT",
}

OP_RELATION = {
    "==" : "EQUALITY_OP",
    "!=" : "INEQUALITY_OP",
    ">" : "GREATER_THAN_OP",
    "<" : "LESS_THAN_OP",
    ">=" : "GREATER_OR_EQUAL_OP",
    "<=" : "LESS_OR_EQUAL_OP",
}

# DELIMITERS
DELIMITERS = {
    ";" : "STMT_TERMINATOR",
    ":" : "CODEBLK_INDICATOR",
    "{" : "OPEN_CURLY_BRACKET",
    "}" : "CLOSE_CURLY_BRACKET",
    "[" : "OPEN_SQUARE_BRACKET",
    "]" : "CLOSE_SQUARE_BRACKET",
    "(" : "OPEN_PARENTHESIS",
    ")" : "CLOSE_PARENTHESIS",
    "\"" : "STRING_DELIMITER",
    "," : "SEPARATOR",
    "." : "OBJECT_DELIMITER"
}

# ESCAPE SEQUENCES
ESCAPE_SEQUENCES = {
    r"\n" : "NEW_LINE",
    r"\t" : "HORIZONTAL_TAB",
    r"\v" : "VERTICAL_TAB",
    r"\'" : "SINGLE_QUOTE",
    r"\"" : "DOUBLE_QUOTE",
    r"\\" : "BACKSLASH"
}

# WHITESPACES
WHITESPACES = {
    " " : "WHITESPACE",
    "\n" : "NEWLINE"
}

# COMMENTS
COMMENTS = {
    "//" : "COMMENT_SINGLE", 
    "/*" : "COMMENT_MULTI_OPEN", 
    "*/" : "COMMENT_MULTI_CLOSE"
}
