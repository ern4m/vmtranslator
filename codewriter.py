import os

def check(e):
    if e is not None:
        raise e

def filename_without_extension(fn):
    return os.path.splitext(fn)[0]

class CodeWriter:
    def __init__(self, path_name):
        self.out = open(path_name, 'w')
        self.module_name = ""
        self.func_name = ""
        self.label_count = 0
        self.call_count = 0
        self.return_sub_count = 0

    def write(self, s):
        self.out.write(f"{s}\n")

    def segment_pointer(self, segment, index):
        if segment == "local":
            return "LCL"
        elif segment == "argument":
            return "ARG"
        elif segment in ["this", "that"]:
            return segment.upper()
        elif segment == "temp":
            return f"R{5 + index}"
        elif segment == "pointer":
            return f"R{3 + index}"
        elif segment == "static":
            return f"{self.module_name}.{index}"
        else:
            return "ERROR"

    def set_file_name(self, path_name):
            self.module_name = os.path.splitext(os.path.basename(path_name))[0]

    def write_push(self, seg, index):
        if seg == "constant":
            self.write(f"@{index} // push {seg} {index}")
            self.write("D=A")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")
        elif seg in ["static", "temp", "pointer"]:
            self.write(f"@{self.segment_pointer(seg, index)} // push {seg} {index}")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")
        elif seg in ["local", "argument", "this", "that"]:
            self.write(f"@{self.segment_pointer(seg, index)} // push {seg} {index}")
            self.write("D=M")
            self.write(f"@{index}")
            self.write("A=D+A")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")

    def write_pop(self, seg, index):
        if seg in ["static", "temp", "pointer"]:
            self.write(f"@SP // pop {seg} {index}")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write(f"@{self.segment_pointer(seg, index)}")
            self.write("M=D")
        elif seg in ["local", "argument", "this", "that"]:
            self.write(f"@{self.segment_pointer(seg, index)} // pop {seg} {index}")
            self.write("D=M")
            self.write(f"@{index}")
            self.write("D=D+A")
            self.write("@R13")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@R13")
            self.write("A=M")
            self.write("M=D")

    def write_arithmetic(self, cmd_name):
        if cmd_name == "add":
            self.write_arithmetic_add()
        elif cmd_name == "sub":
            self.write_arithmetic_sub()
        elif cmd_name == "neg":
            self.write_arithmetic_neg()
        elif cmd_name == "eq":
            self.write_arithmetic_eq()
        elif cmd_name == "gt":
            self.write_arithmetic_gt()
        elif cmd_name == "lt":
            self.write_arithmetic_lt()
        elif cmd_name == "and":
            self.write_arithmetic_and()
        elif cmd_name == "or":
            self.write_arithmetic_or()
        elif cmd_name == "not":
            self.write_arithmetic_not()

    def write_binary_arithmetic(self):
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("A=A-1")

    def write_arithmetic_add(self):
        self.write_binary_arithmetic()
        self.write("M=D+M")

    def write_arithmetic_sub(self):
        self.write_binary_arithmetic()
        self.write("M=M-D")

    def write_arithmetic_and(self):
        self.write_binary_arithmetic()
        self.write("M=D&M")

    def write_arithmetic_or(self):
        self.write_binary_arithmetic()
        self.write("M=D|M")

    def write_unary_arithmetic(self):
        self.write("@SP")
        self.write("A=M")
        self.write("A=A-1")

    def write_arithmetic_neg(self):
        self.write_unary_arithmetic()
        self.write("M=-M")

    def write_arithmetic_not(self):
        self.write_unary_arithmetic()
        self.write("M=!M")

    def set_file_name(self, path_name):
        self.module_name = os.path.splitext(os.path.basename(path_name))[0]

    def close_file(self):
        self.out.close()
