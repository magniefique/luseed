from python_rep import *

class SyntacticAnalyzer:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.parsed_code = ""
        self.analyze()

    def analyze(self):
        for token in self.tokens:
            if token[0] in CODE_REP:
                self.parsed_code += CODE_REP[token[0]]
            elif token[0] == ";":
                self.parsed_code += "\n"
            else:
                self.parsed_code += token[0]
        self.run()

    def run(self):
        exec(self.parsed_code)