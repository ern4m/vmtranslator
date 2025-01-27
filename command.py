from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def is_command(self):
        pass

class Arithmetic(Command):
    def __init__(self, name):
        self.name = name

    def is_command(self):
        pass

class Pop(Command):
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    def is_command(self):
        pass

class Push(Command):
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    def is_command(self):
        pass

class Label(Command):
    def __init__(self, name):
        self.name = name

    def is_command(self):
        pass

class Goto(Command):
    def __init__(self, label):
        self.label = label

    def is_command(self):
        pass

class IfGoto(Command):
    def __init__(self, label):
        self.label = label

    def is_command(self):
        pass

class Function(Command):
    def __init__(self, name, vars):
        self.name = name
        self.vars = vars

    def is_command(self):
        pass

class CallFunction(Command):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def is_command(self):
        pass

class Return(Command):
    def is_command(self):
        pass

class UndefinedCommand(Command):
    def __init__(self, label):
        self.label = label

    def is_command(self):
        pass
