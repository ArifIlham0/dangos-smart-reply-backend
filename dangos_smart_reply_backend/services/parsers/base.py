from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse(self, html: str) -> list:
        pass

def get_parser(platform: str):
    if platform == "notion":
        from .notion import NotionParser
        
        return NotionParser()
    raise ValueError("Parser not found")