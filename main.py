
import os
import sys
import logging
from pathlib import Path
from codewriter import CodeWriter
from parser import Parser
from command import (
    Arithmetic,
    Push,
    Pop,
    Label,
    Goto,
    IfGoto,
    Return,
    CallFunction,
    Function,
)

def is_directory(path):
    return Path(path).is_dir()

def filename_without_extension(file_path):
    return Path(file_path).stem

def translate(file_path, code_writer):
    parser = Parser(file_path)
    code_writer.set_file_name(file_path)
    while parser.has_more_commands():
        cmd = parser.next_command()
        if isinstance(cmd, Arithmetic):
            code_writer.write_arithmetic(cmd)
        elif isinstance(cmd, Push):
            code_writer.write_push(cmd.segment, cmd.index)
        elif isinstance(cmd, Pop):
            code_writer.write_pop(cmd.segment, cmd.index)
        elif isinstance(cmd, Label):
            code_writer.write_label(cmd.name)
        elif isinstance(cmd, Goto):
            code_writer.write_goto(cmd.label)
        elif isinstance(cmd, IFGoto):
            code_writer.write_if(cmd.label)
        elif isinstance(cmd, Return):
            code_writer.write_return()
        elif isinstance(cmd, CallFunction):
            code_writer.write_call(cmd.func_name, cmd.args)
        elif isinstance(cmd, Function):
            code_writer.write_function(cmd.name, cmd.vars)

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <path>")
        sys.exit(1)

    path = sys.argv[1]

    if is_directory(path):
        code_writer = CodeWriter(f"{filename_without_extension(path)}/{Path(path).name}.asm")
        code_writer.write_init()
        for file in Path(path).iterdir():
            if file.suffix == ".vm":
                abs_path = file.resolve()
                print(f"Translating: {abs_path}")
                translate(abs_path, code_writer)
        code_writer.close_file()
    else:
        abs_path = Path(path).resolve()
        print(f"Translating: {abs_path}")
        code_writer = CodeWriter(f"{filename_without_extension(path)}.asm")
        code_writer.write_init()
        translate(abs_path, code_writer)
        code_writer.close_file()

if __name__ == "__main__":
    main()
