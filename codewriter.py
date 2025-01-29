class CodeWriter:
    def __init__(self, file_name):
        self.writer = open(file_name, "w")
        self.module_name = ""
        self.syn_count = 0

    def set_file_name(self, file_name):
        self.module_name = file_name.split("/")[-1].split(".")[0]

    def register_name(self, segment, index):
        if segment == "local":
            return "LCL"
        elif segment == "argument":
            return "ARG"
        elif segment == "this":
            return "THIS"
        elif segment == "that":
            return "THAT"
        elif segment == "pointer":
            return f"R{3 + index}"
        elif segment == "temp":
            return f"R{5 + index}"
        else:
            return f"{self.module_name}.{index}"

    def write_push(self, segment, index):
        if segment == "constant":
            self._write(f"@{index} // push {segment} {index}")
            self._write("D=A")
            self._write("@SP")
            self._write("A=M")
            self._write("M=D")
            self._write("@SP")
            self._write("M=M+1")
        elif segment in ["static", "temp", "pointer"]:
            self._write(f"@{self.register_name(segment, index)} // push {segment} {index}")
            self._write("D=M")
            self._write("@SP")
            self._write("A=M")
            self._write("M=D")
            self._write("@SP")
            self._write("M=M+1")
        else:
            self._write(f"@{self.register_name(segment, 0)} // push {segment} {index}")
            self._write("D=M")
            self._write(f"@{index}")
            self._write("A=D+A")
            self._write("D=M")
            self._write("@SP")
            self._write("A=M")
            self._write("M=D")
            self._write("@SP")
            self._write("M=M+1")

    def write_pop(self, segment, index):
        if segment in ["static", "temp", "pointer"]:
            self._write("@SP // pop {segment} {index}")
            self._write("M=M-1")
            self._write("A=M")
            self._write("D=M")
            self._write(f"@{self.register_name(segment, index)}")
            self._write("M=D")
        else:
            self._write(f"@{self.register_name(segment, 0)} // pop {segment} {index}")
            self._write("D=M")
            self._write(f"@{index}")
            self._write("D=D+A")
            self._write("@R13")
            self._write("M=D")
            self._write("@SP")
            self._write("M=M-1")
            self._write("A=M")
            self._write("D=M")
            self._write("@R13")
            self._write("A=M")
            self._write("M=D")

    def write_arithmetic(self, command):
        if command == "add":
            self._write_arithmetic_add()
        elif command == "sub":
            self._write_arithmetic_sub()
        elif command == "neg":
            self._write_arithmetic_neg()
        elif command == "eq":
            self._write_arithmetic_eq()
        elif command == "gt":
            self._write_arithmetic_gt()
        elif command == "lt":
            self._write_arithmetic_lt()
        elif command == "and":
            self._write_arithmetic_and()
        elif command == "or":
            self._write_arithmetic_or()
        else:
            self._write_arithmetic_not()

    def _write_arithmetic_add(self):
        self._write("@SP // add")
        self._write("M=M-1")
        self._write("A=M")
        self._write("D=M")
        self._write("A=A-1")
        self._write("M=D+M")

    def _write_arithmetic_sub(self):
        self._write("@SP // sub")
        self._write("M=M-1")
        self._write("A=M")
        self._write("D=M")
        self._write("A=A-1")
        self._write("M=M-D")

    def _write_arithmetic_neg(self):
        self._write("@SP // neg")
        self._write("A=M")
        self._write("A=A-1")
        self._write("M=-M")

    def _write_arithmetic_and(self):
        self._write("@SP // and")
        self._write("AM=M-1")
        self._write("D=M")
        self._write("A=A-1")
        self._write("M=D&M")

    def _write_arithmetic_or(self):
        self._write("@SP // or")
        self._write("AM=M-1")
        self._write("D=M")
        self._write("A=A-1")
        self._write("M=D|M")

    def _write_arithmetic_not(self):
        self._write("@SP // not")
        self._write("A=M")
        self._write("A=A-1")
        self._write("M=!M")

    def _write_arithmetic_eq(self):
        label = f"JEQ_{self.module_name}_{self.syn_count}"
        self.syn_count += 1
        self._write("@SP // eq")
        self._write("AM=M-1")
        self._write("D=M")
        self._write("@SP")
        self._write("AM=M-1")
        self._write("D=M-D")
        self._write(f"@{label}")
        self._write("D;JEQ")
        self._write("D=1")
        self._write(f"({label})")
        self._write("D=D-1")
        self._write("@SP")
        self._write("A=M")
        self._write("M=D")
        self._write("@SP")
        self._write("M=M+1")

    def _write_arithmetic_gt(self):
        label_true = f"JGT_TRUE_{self.module_name}_{self.syn_count}"
        label_false = f"JGT_FALSE_{self.module_name}_{self.syn_count}"
        self.syn_count += 1
        self._write("@SP // gt")
        self._write("AM=M-1")
        self._write("D=M")
        self._write("@SP")
        self._write("AM=M-1")
        self._write("D=M-D")
        self._write(f"@{label_true}")
        self._write("D;JGT")
        self._write("D=0")
        self._write(f"@{label_false}")
        self._write("0;JMP")
        self._write(f"({label_true})")
        self._write("D=-1")
        self._write(f"({label_false})")
        self._write("@SP")
        self._write("A=M")
        self._write("M=D")
        self._write("@SP")
        self._write("M=M+1")

    def _write_arithmetic_lt(self):
        label_true = f"JLT_TRUE_{self.module_name}_{self.syn_count}"
        label_false = f"JLT_FALSE_{self.module_name}_{self.syn_count}"
        self.syn_count += 1
        self._write("@SP // lt")
        self._write("AM=M-1")
        self._write("D=M")
        self._write("@SP")
        self._write("AM=M-1")
        self._write("D=M-D")
        self._write(f"@{label_true}")
        self._write("D;JLT")
        self._write("D=0")
        self._write(f"@{label_false}")
        self._write("0;JMP")
        self._write(f"({label_true})")
        self._write("D=-1")
        self._write(f"({label_false})")
        self._write("@SP")
        self._write("A=M")
        self._write("M=D")
        self._write("@SP")
        self._write("M=M+1")

    def close(self):
        self.writer.close()

    def _write(self, s):
        self.writer.write(s + "\n")
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()