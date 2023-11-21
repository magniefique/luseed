import regex
UPPERC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERC = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
SPECIAL_CHAR = [".", "+", "-", "*", "/", "%", "<", ">", "=", "\"", "\'", ",", ";", "|", "!", "(", ")", "[", "]", "{", "}", "_", "^", "~", "&", ":", "?", "^", "#", "@", "-", "`"]
DOUBLE_OP = ["+", "-", "*", "/", "%", "~", "=", "!", "<", ">"]

# KEYWORD DICTIONARY
KEYWORDS = {
    "ask" : "keyword",
    "bool" : "keyword",
    "break" : "keyword",
    "char" : "keyword",
    "class" : "keyword",
    "const" : "keyword",
    "continue" : "keyword",
    "display" : "keyword",
    "do" : "keyword",
    "double" : "keyword",
    "elif" : "keyword",
    "else" : "keyword",
    "false" : "keyword",
    "float" : "keyword",
    "for" : "keyword",
    "func" : "keyword",
    "if" : "keyword",
    "init" : "keyword",
    "int" : "keyword",
    "list" : "keyword",
    "obj" : "keyword",
    "private" : "keyword",
    "protected" : "keyword",
    "public" : "keyword",
    "repeat" : "keyword",
    "return" : "keyword",
    "str" : "keyword",
    "then" : "keyword",
    "this" : "keyword",
    "true" : "keyword",
    "until" : "keyword",
    "while" : "keyword"
}

# OPERATORS
OP_ASSIGNMENT = {
    "=" : "assignment_op",
    "+=" : "addition_assignment_op",
    "-=" : "subtraction_assignment_op",
    "*=" : "multiplication_assignment_op",
    "/=" : "division_assignment_op",
    "%=" : "modulo_assignment_op",
    "~=" : "floor_division_assignment_op"
}

OP_ARITHMETIC = {
    "+" : "addition_op",
    "-" : "subtraction_op",
    "*" : "multiplication_op",
    "/" : "division_op",
    "%" : "modulo_op",
    "~" : "floor_division_op",
    "**" : "exponentiate_op"
}

OP_UNARY = {
    "+" : "positive_op",
    "-" : "negative_op", 
    "++" : "increment_op",
    "--" : "decrement_op",
}

OP_LOGIC = {
    "not" : "not_op",
    "or" : "or_op",
    "and" : "and_op"
}

OP_RELATION = {
    "==" : "equality_op",
    "!=" : "inequality_op",
    ">" : "greater_than_op",
    "<" : "less_than_op",
    ">=" : "greater_or_equal_op",
    "<=" : "less_or_equal_op",
}

# DELIMITERS
DELIMITERS = {
    ";" : "statement_terminator",
    ":" : "code_block_indicator",
    "{" : "open_curly_bracket",
    "}" : "close_curly_bracket",
    "[" : "open_square_bracket",
    "]" : "close_square_bracket",
    "(" : "open_parenthesis",
    ")" : "close_parenthesis",
    "\"" : "string_delimiter"
}

# ESCAPE SEQUENCES
ESCAPE_SEQUENCES = {
    r"\n" : "new_line",
    r"\t" : "horizontal_tab",
    r"\v" : "vertical_tab",
    r"\'" : "single_quote",
    r"\"" : "double_quote",
}

# WHITESPACES
WHITESPACES = {
    " " : "whitespace"
}
