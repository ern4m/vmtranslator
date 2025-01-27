import re
from command import (
    Return,
    Arithmetic,
    Label,
    Goto,
    IfGoto,
    Push,
    Pop,
    Function,
    CallFunction,
    UndefinedCommand,
)

class Parser:
    def __init__(self, fname):
        self.tokens = []
        self.position = 0
        self.curr_token = ""
        self._tokenize_file(fname)

    def _tokenize_file(self, fname):
        with open(fname, 'r') as file:
            code = file.read()
        code_proc = re.sub(r'//.*', '', code)
        self.tokens = re.findall(r'[a-zA-Z][_a-zA-Z0-9./-]*|0|[1-9][0-9]*', code_proc)

    def has_more_commands(self):
        return self.position < len(self.tokens)

    def advance(self):
        self.curr_token = self.tokens[self.position]
        self.position += 1

    def next_command(self):
        self.advance()
        if self.curr_token == "return":
            return Return()
        elif self.curr_token in {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}:
            return Arithmetic(name=self.curr_token)
        elif self.curr_token in {"label", "if-goto", "goto"}:
            cmd = self.curr_token
            self.advance()
            arg1 = self.curr_token
            if cmd == "label":
                return Label(name=arg1)
            elif cmd == "goto":
                return Goto(label=arg1)
            elif cmd == "if-goto":
                return IFGoto(label=arg1)
        elif self.curr_token in {"push", "pop", "function", "call"}:
            cmd = self.curr_token
            self.advance()
            arg1 = self.curr_token
            self.advance()
            arg2 = int(self.curr_token)
            if cmd == "push":
                return Push(segment=arg1, index=arg2)
            elif cmd == "pop":
                return Pop(segment=arg1, index=arg2)
            elif cmd == "function":
                return Function(name=arg1, vars=arg2)
            elif cmd == "call":
                return CallFunction(func_name=arg1, args=arg2)
        return UndefinedCommand()

