class Parser:
    RULES = [
        ["dataType_3", ["KW_PROT"]],
        ["dataType_2", ["KW_PRIV"]],
        ["dataType_1", ["KW_PUB"]],
        ["decType", ["IDENTIFIER"]],
        ["decList", ["decType"]],
        ["dec_stmnt", ["dataType", "decList"]],
    ]

    def __init__(self, token_list) -> None:
        self.token_list = token_list
        self.stack = []
        self.stack_ctr = 0
        self.checkval = ""
        self.idx_ctr = -1
        self.idx_incr()

    def idx_incr(self):
        self.idx_ctr += 1
        if self.idx_ctr < len(self.token_list):
            self.current_token = self.token_list[self.idx_ctr]
        
        return self.current_token
    
    def parse(self):
        print(self.add_stack())

    def add_stack(self):
        self.stack.append(self.token_list.pop(0))
        self.reduce()
        return self.stack

    def reduce(self):
        for i in range(len(Parser.RULES)):
            for j in range(len(Parser.RULES[i][1])):
                try:
                    if self.stack[self.stack_ctr] == Parser.RULES[i][1][j]:
                        self.checkval += "1"
                    else:
                        self.checkval += "0"
                except:
                    continue
            
            if "0" not in self.checkval:
                self.stack[self.stack_ctr] = Parser.RULES[i][0] if "_" not in Parser.RULES[i][0][-2:] else Parser.RULES[i][0][:-2]

            self.checkval = ""

        self.reduce_stack()

        if self.token_list != []:
            self.stack_ctr +=1
            self.add_stack()

    def reduce_stack(self):
        for i in range(len(Parser.RULES)):
            for j in range(len(Parser.RULES[i][1])):
                try:
                    if self.stack[self.stack_ctr] == Parser.RULES[i][1][j]:
                        self.checkval += "1"
                        break
                    else:
                        self.checkval += "0"
                except:
                    continue
            
            if "0" not in self.checkval:
                self.stack[self.stack_ctr] = Parser.RULES[i][0] if "_" not in Parser.RULES[i][0][-2:] else Parser.RULES[i][0][:-2]

            self.checkval = ""
        return

obj = Parser(["KW_PROT", "IDENTIFIER"])
obj.parse()