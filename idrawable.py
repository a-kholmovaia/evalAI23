from abc import ABC, abstractmethod
from window import Window

class IDrawable(ABC):
    @abstractmethod
    def draw(self, window: Window):
        pass
    
    @abstractmethod
    def resize(self, window: Window):
        pass