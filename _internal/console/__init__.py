from rich import print


class Logger:
    def __init__(self, name):
        self.name = name

    def info(self, message):
        print(f"[bold blue] {self.name} [/bold blue] {message}")

    def error(self, message):
        print(f"[bold red] {self.name} [/bold red] {message}")

    def success(self, message):
        print(f"[bold green] {self.name} [/bold green] {message}")

    def warning(self, message):
        print(f"[bold yellow] {self.name} [/bold yellow] {message}")