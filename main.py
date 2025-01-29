import sys
from parser import Parser
from codewriter import CodeWriter

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <inputFile.vm>")
        return

    input_file_name = sys.argv[1]
    output_file_name = input_file_name.replace(".vm", ".asm")

    try:
        with Parser(input_file_name) as parser, CodeWriter(output_file_name) as code_writer:
            while parser.has_more_commands():
                parser.advance()
                command_type = parser.command_type()

                if command_type == "C_ARITHMETIC":
                    code_writer.write_arithmetic(parser.arg1())
                elif command_type == "C_PUSH":
                    code_writer.write_push(parser.arg1(), parser.arg2())
                elif command_type == "C_POP":
                    code_writer.write_pop(parser.arg1(), parser.arg2())
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()