
class File:
    def __init__(self, path: str) -> None:
        self.path = path
        self.content = None
        self.ast = None
        self.file = open(self.path, 'r')

    def get_content(self):
        if self.content is None:
            self.content = self.file.read()
        return self.content
    
    def close(self):
        self.file.close()
        self.content = None