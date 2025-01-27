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

    def write_init(self):
        self.write("@256")
        self.write("D=A")
        self.write("@SP")
        self.write("M=D")
        self.write_call("Sys.init", 0)
        self.write_subroutine_return()
        self.write_sub_arithmetic_lt()
        self.write_sub_arithmetic_gt()
        self.write_sub_arithmetic_eq()
        self.write_sub_frame()

    def write_sub_frame(self):
        self.write("($FRAME$)")
        self.write("@R15")
        self.write("M=D")
        self.write_frame_push("LCL")
        self.write_frame_push("ARG")
        self.write_frame_push("THIS")
        self.write_frame_push("THAT")
        self.write("@R15")
        self.write("A=M")
        self.write("0;JMP")

    def write_subroutine_return(self):
        self.write("($RETURN$)")
        self.write("@R15")
        self.write("M=D")
        # FRAME = LCL
        self.write("@LCL")
        self.write("D=M")
        self.write("@R13")  # R13 -> FRAME
        self.write("M=D")
        # RET = *(FRAME-5)
        self.write("@5")
        self.write("A=D-A")
        self.write("D=M")
        self.write("@R14")  # R14 -> RET
        self.write("M=D")
        # *ARG = pop()
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@ARG")
        self.write("A=M")
        self.write("M=D")
        # SP = ARG+1
        self.write("D=A")
        self.write("@SP")
        self.write("M=D+1")
        # THAT = *(FRAME-1)
        self.write("@R13")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@THAT")
        self.write("M=D")
        # THIS = *(FRAME-2)
        self.write("@R13")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@THIS")
        self.write("M=D")
        # ARG = *(FRAME-3)
        self.write("@R13")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@ARG")
        self.write("M=D")
        # LCL = *(FRAME-4)
        self.write("@R13")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@LCL")
        self.write("M=D")
        # goto RET
        self.write("@R14")
        self.write("A=M")
        self.write("0;JMP")
        self.write("@R15")
        self.write("A=M")
        self.write("0;JMP")

    def write_sub_arithmetic_eq(self):
        self.write("($EQ$)")
        self.write("@R15")
        self.write("M=D")
        label = f"JEQ_{self.module_name}_{self.label_count}"
        self.write("@SP // eq")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write(f"@{label}")
        self.write("D;JEQ")
        self.write("D=1")
        self.write(f"({label})")
        self.write("D=D-1")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
        self.label_count += 1
        self.write("@R15")
        self.write("A=M")
        self.write("0;JMP")

    def write_sub_arithmetic_gt(self):
        self.write("($GT$)")
        self.write("@R15")
        self.write("M=D")
        label_true = f"JGT_TRUE_{self.module_name}_{self.label_count}"
        label_false = f"JGT_FALSE_{self.module_name}_{self.label_count}"
        self.write("@SP // gt")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write(f"@{label_true}")
        self.write("D;JGT")
        self.write("D=0")
        self.write(f"@{label_false}")
        self.write("0;JMP")
        self.write(f"({label_true})")
        self.write("D=-1")
        self.write(f"({label_false})")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
        self.label_count += 1
        self.write("@R15")
        self.write("A=M")
        self.write("0;JMP")

    def write_sub_arithmetic_lt(self):
        self.write("($LT$)")
        self.write("@R15")
        self.write("M=D")
        label_true = f"JLT_TRUE_{self.module_name}_{self.label_count}"
        label_false = f"JLT_FALSE_{self.module_name}_{self.label_count}"
        self.write("@SP // lt")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M-D")
        self.write(f"@{label_true}")
        self.write("D;JLT")
        self.write("D=0")
        self.write(f"@{label_false}")
        self.write("0;JMP")
        self.write(f"({label_true})")
        self.write("D=-1")
        self.write(f"({label_false})")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
        self.label_count += 1
        self.write("@R15")
        self.write("A=M")
        self.write("0;JMP")

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

    def write_arithmetic_eq(self):
        return_addr = f"$RET{self.return_sub_count}"
        self.write(f"@{return_addr}")
        self.write("D=A")
        self.write("@$EQ$")
        self.write("0;JMP")
        self.write(f"({return_addr})")
        self.return_sub_count += 1

    def write_arithmetic_gt(self):
        return_addr = f"$RET{self.return_sub_count}"
        self.write(f"@{return_addr}")
        self.write("D=A")
        self.write("@$GT$")
        self.write("0;JMP")
        self.write(f"({return_addr})")
        self.return_sub_count += 1

    def write_arithmetic_lt(self):
        return_addr = f"$RET{self.return_sub_count}"
        self.write(f"@{return_addr}")
        self.write("D=A")
        self.write("@$LT$")
        self.write("0;JMP")
        self.write(f"({return_addr})")
        self.return_sub_count += 1
    def set_file_name(self, path_name):
        self.module_name = os.path.splitext(os.path.basename(path_name))[0]

    def write_label(self, label):
        new_label = f"{self.func_name}${label}"
        self.write(f"({new_label})")

    def write_goto(self, label):
        new_label = f"{self.func_name}${label}"
        self.write(f"@{new_label}")
        self.write("0;JMP")

    def write_if(self, label):
        new_label = f"{self.func_name}${label}"
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("M=0")
        self.write(f"@{new_label}")
        self.write("D;JNE")

    def write_function(self, func_name, n_locals):
        loop_label = f"{func_name}_INIT_LOCALS_LOOP"
        loop_end_label = f"{func_name}_INIT_LOCALS_END"

        self.func_name = func_name

        self.write(f"({func_name}) // initialize local variables")
        self.write(f"@{n_locals}")
        self.write("D=A")
        self.write("@R13")  # temp
        self.write("M=D")
        self.write(f"({loop_label})")
        self.write(f"@{loop_end_label}")
        self.write("D;JEQ")
        self.write("@0")
        self.write("D=A")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")
        self.write("@R13")
        self.write("MD=M-1")
        self.write(f"@{loop_label}")
        self.write("0;JMP")
        self.write(f"({loop_end_label})")

    def write_frame_push(self, value):
        self.write(f"@{value}")
        self.write("D=M")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")

    def write_call(self, func_name, num_args):
        comment = f"// call {func_name} {num_args}"
        return_addr = f"{func_name}_RETURN_{self.call_count}"
        self.call_count += 1

        self.write(f"@{return_addr} {comment}")  # push return-addr
        self.write("D=A")
        self.write("@SP")
        self.write("A=M")
        self.write("M=D")
        self.write("@SP")
        self.write("M=M+1")

        # Push the LCL, ARG, THIS, THAT registers
        self.write_frame_push("LCL")
        self.write_frame_push("ARG")
        self.write_frame_push("THIS")
        self.write_frame_push("THAT")

        # Reposition ARG = SP - n - 5
        self.write(f"@{num_args}")
        self.write("D=A")
        self.write("@5")
        self.write("D=D+A")
        self.write("@SP")
        self.write("D=M-D")
        self.write("@ARG")
        self.write("M=D")

        # Set LCL = SP
        self.write("@SP")
        self.write("D=M")
        self.write("@LCL")
        self.write("M=D")

        # Goto the function
        self.write(f"@{func_name}")
        self.write("0;JMP")

        # Declare return address label
        self.write(f"({return_addr})")

    def write_return(self):
        return_addr = f"$RET{self.return_sub_count}"
        self.write(f"@{return_addr}")
        self.write("D=A")
        self.write("@$RETURN$")
        self.write("0;JMP")
        self.write(f"({return_addr})")
        self.return_sub_count += 1

    def close_file(self):
        self.out.close()
