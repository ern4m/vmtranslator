class Parser:
    def __init__(self, file_name):
        self.reader = open(file_name, "r")
        self.current_command = None

    def has_more_commands(self):
        # Check if there are more lines to read
        current_position = self.reader.tell()
        has_more = bool(self.reader.readline())
        self.reader.seek(current_position)  # Reset the file pointer
        return has_more

    def advance(self):
        if self.has_more_commands():
            self.current_command = self.reader.readline().strip()
            # Skip empty lines and comments
            while self.current_command and (self.current_command == "" or self.current_command.startswith("//")):
                self.current_command = self.reader.readline().strip()
        else:
            self.current_command = None

    def command_type(self):
        if not self.current_command:
            return None
        if self.current_command.startswith("push"):
            return "C_PUSH"
        elif self.current_command.startswith("pop"):
            return "C_POP"
        elif self.current_command.startswith("label"):
            return "C_LABEL"
        elif self.current_command.startswith("goto"):
            return "C_GOTO"
        elif self.current_command.startswith("if-goto"):
            return "C_IF"
        elif self.current_command.startswith("function"):
            return "C_FUNCTION"
        elif self.current_command.startswith("call"):
            return "C_CALL"
        elif self.current_command.startswith("return"):
            return "C_RETURN"
        else:
            return "C_ARITHMETIC"

    def arg1(self):
        if self.command_type() == "C_RETURN":
            raise ValueError("arg1() called on C_RETURN command")
        if self.command_type() == "C_ARITHMETIC":
            return self.current_command
        return self.current_command.split(" ")[1]

    def arg2(self):
        if self.command_type() not in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            raise ValueError("arg2() called on invalid command type")
        return int(self.current_command.split(" ")[2])

    def close(self):
        self.reader.close()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()