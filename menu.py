import re
from kivy.uix.relativelayout import RelativeLayout

class MenuWidget(RelativeLayout):
    """Class to create the relative layout"""
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout,self).on_touch_down(touch)

