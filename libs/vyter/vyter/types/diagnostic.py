class Diagnostic:
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"[{self.line}:{self.column}] {self.message}"