from window import Window

class DrawableObject():

    def __init__(self, window: Window, x: int, y: int, width: int, height: int):
        self.window = window
        self.original_x = x
        self.original_y = y
        self.original_width = width
        self.original_height = height

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        

    def draw(self):
        #Abstract method
        pass
    
    
    def scale(self):
        self.x = self.original_x * self.window.get_scale()
        self.y = self.original_y * self.window.get_scale()
        self.width = self.original_width * self.window.get_scale()
        self.height = self.original_height * self.window.get_scale()

        self.original_x = self.x
        self.original_y = self.y
        self.original_width = self.width
        self.original_height = self.height

        self.draw()