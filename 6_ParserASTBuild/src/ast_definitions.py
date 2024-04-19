from lexer import tokens


class ASTNode:
    def __init__(self, name):
        self.name = name


class StartCommand(ASTNode):
    def __init__(self, command, target_flag, command_sequence):
        super().__init__(command)
        self.target_flag = target_flag
        self.command_sequence = command_sequence


class TargetFlag(ASTNode):
    def __init__(self, flag, path):
        super().__init__(flag)
        self.value = path


class Command(ASTNode):
    def __init__(self, command, flags=None, next_command=None):
        super().__init__(command)
        self.flags = flags or []
        self.next_command = next_command  # Optional next command


class Flag(ASTNode):
    def __init__(self, flag, value):
        super().__init__(flag)
        self.value = value
