from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, ColorProperty, StringProperty

from .mode import Mode

class Tool(Button):
    def on_pixel_down(self, pixel):
        pass
        
    def on_pixel_move(self, pixel):
        pass
        
    def on_pixel_up(self, pixel):
        pass
    
    def on_pixel_hover(self, pixel):
        pass
            
    @property
    def name(self):
        return type(self).__name__
    
    
class Pencil(Tool):
    def on_pixel_hover(self, pixel):
        pixel.color = self.root.color.color

        
class Eraser(Tool):
    def on_pixel_hover(self, pixel):
        pixel.color = 0, 0, 0
    
    
class Dropper(Tool):
    def on_pixel_hover(self, pixel):
        self.root.color.color = pixel.color
    

class Paint(Mode):
    NAME = "Paint"

    color = ObjectProperty(None)
    tool = ObjectProperty(None)
    grid = ObjectProperty(None)

    def on_activated(self):
        self.grid.clear()
        self.grid.children[0].color = (255, 255, 0)
        self.grid.children[12].color = (0, 255, 0)
        self.grid.children[39].color = (255, 0, 0)

    def on_deactivated(self):
        pass

    def on_pixel_down(self, pixel):
        self.tool.on_pixel_down(pixel)
        self.tool.on_pixel_hover(pixel)

    def on_pixel_move(self, pixel):
        self.tool.on_pixel_move(pixel)
        self.tool.on_pixel_hover(pixel)
        
    def on_pixel_up(self, pixel):
        self.tool.on_pixel_up(pixel)
        
    def update(self, dt):
        pass


class PaintTools(GridLayout):
    def pick_tool(self, touch, name):
        if self.collide_point(*touch.pos):
            self.parent.parent.current_tool = name
