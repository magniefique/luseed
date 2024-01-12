SPECIAL_CHAR = [".", "+", "-", "*", "/", "%", "<", ">", "=", "\\", "\"", "\'", ",", ";", "|", "!", "(", ")", "[", "]", "{", "}", "_", "^", "~", "&", ":", "?", "^", "#", "@", "-", "`"]
DOUBLE_OP = ["+", "-", "*", "/", "%", "~", "=", "!", "<", ">"]
ESCAPE_CHAR = ["n", "t", "v", "\'", "\"", "\\"]

# KEYWORD DICTIONARY
KEYWORDS = {
    "ask" : "KEYWORD",
    "bool" : "KEYWORD",
    "break" : "KEYWORD",
    "char" : "KEYWORD",
    "class" : "KEYWORD",
    "const" : "KEYWORD",
    "continue" : "KEYWORD",
    "display" : "KEYWORD",
    "do" : "KEYWORD",
    "double" : "KEYWORD",
    "elif" : "KEYWORD",
    "else" : "KEYWORD",
    "false" : "KEYWORD",
    "float" : "KEYWORD",
    "for" : "KEYWORD",
    "foreach" : "KEYWORD",
    "func" : "KEYWORD",
    "help" : "KEYWORD",
    "if" : "KEYWORD",
    "info" : "KEYWORD",
    "init" : "KEYWORD",
    "inheritall" : "KEYWORD",
    "in" : "KEYWORD",
    "int" : "KEYWORD",
    "list" : "KEYWORD",
    "main" : "KEYWORD",
    "null" : "KEYWORD",
    "obj" : "KEYWORD",
    "pass" : "KEYWORD",
    "private" : "KEYWORD",
    "protected" : "KEYWORD",
    "public" : "KEYWORD",
    "quit" : "KEYWORD",
    "repeat" : "KEYWORD",
    "return" : "KEYWORD",
    "str" : "KEYWORD",
    "then" : "KEYWORD",
    "this" : "KEYWORD",
    "true" : "KEYWORD",
    "until" : "KEYWORD",
    "while" : "KEYWORD"
}

# NOISEWORDS
NOISEWORDS = {
    "boolean" : "KEYWORD",
    "character" : "KEYWORD",
    "constant" : "KEYWORD",
    "integer" : "KEYWORD",
    "information" : "KEYWORD",
    "initialize" : "KEYWORD",
    "object" : "KEYWORD",
    "string" : "KEYWORD"
}

# OPERATORS
OP_ASSIGNMENT = {
    "=" : "ASSIGNMENT_OP",
    "+=" : "ADDITION_ASSIGNMENT_OP",
    "-=" : "SUBTRACTION_ASSIGNMENT_OP",
    "*=" : "MULTIPLICATION_ASSIGNMENT_OP",
    "/=" : "DIVISION_ASSIGNMENT_OP",
    "%=" : "MODULO_ASSIGNMENT_OP",
    "~=" : "FLRDIVISION_ASSIGNMENT_OP"
}

OP_ARITHMETIC = {
    "+" : "ADDITION_OP",
    "-" : "SUBTRACTION_OP",
    "*" : "MULTIPLICATION_OP",
    "/" : "DIVISION_OP",
    "%" : "MODULO_OP",
    "~" : "FLRDIVISION_OP",
    "**" : "EXPONENTIATE_OP"
}

OP_UNARY = {
    "+" : "POSITIVE_OP",
    "-" : "NEGATIVE_OP", 
    "++" : "INCREMENT_OP",
    "--" : "DECREMENT_OP",
}

OP_LOGIC = {
    "not" : "NOT_OP",
    "or" : "OR_OP",
    "and" : "AND_OP"
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
    " " : "WHITESPACE"
}

# COMMENTS
COMMENTS = ["//", "/*", "*/"]
