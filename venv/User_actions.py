
from kivy.uix.relativelayout import RelativeLayout


def on_touch_down(self, touch):
    if not self.GAME_OVER and self.GAME_STARTED:
        if touch.x <= self.width /2:
            self.current_speed_x = self.SPEED_X

        else:
            self.current_speed_x = -self.SPEED_X

    return super(RelativeLayout,self).on_touch_down(touch)
            

def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self.current_speed_x = 0
    
def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.current_speed_x = self.SPEED_X
    elif keycode[1] == 'right':
        self.current_speed_x = -self.SPEED_X
    return True

def on_keyboard_up(self,*args):
    self.current_speed_x = 0
    return True
def on_touch_up(self, touch):
    self.current_speed_x = 0
    print("REALEASED!!")