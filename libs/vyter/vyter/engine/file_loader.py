import os
from typing import List
from ..types.file import File

class FileLoader:
    def __init__(self, root_path: str) -> None:
        self.root_path = root_path
    
    def load_files(self) -> List[File]:
        found_files = []
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if file.endswith('.vy'):
                    found_files.append(File(os.path.join(root, file)))
        return found_files