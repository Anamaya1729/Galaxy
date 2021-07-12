from kivy.config import Config
Config.set("graphics","width",1200)
Config.set("graphics","width",400)
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.metrics import sp
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window

class MainWidget(Widget):
    perspectivePoint_x = NumericProperty(0)
    perspectivePoint_y = NumericProperty(0)
    howManyVerticalLines = 12
    v_spacing = .25# Percentage in screen width
    VerticalLinesList = []

    howManyHorizontalLines = 10
    h_spacing = .1 #Percentage in screen height
    HorizontalLinesList = []

    current_offset_y = 0

    SPEED = 4
    SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.initVerticalLines()
        self.initHorizontalLines()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up = self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def on_size(self, *args):
        pass

    def initVerticalLines(self):
        with self.canvas:
            Color(1,1,1)
            for _ in range(self.howManyVerticalLines):
                self.VerticalLinesList.append(Line())
    
    def verticalLinesUpdate(self):
        center_x = int(self.width/2)
        offset = int(-self.howManyVerticalLines/2) + 0.5
        spacing = int(self.width * self.v_spacing)

        for i in range(self.howManyVerticalLines):
            line_x = int(center_x + offset*spacing + self.current_offset_x)
            x1,y1 = self.transform(line_x,0)
            x2,y2 = self.transform(line_x,self.height)
            self.VerticalLinesList[i].points = [x1, y1, x2, y2]
            offset +=1
    
    def initHorizontalLines(self):
        with self.canvas:
            Color(1,1,1)
            for _ in range(self.howManyHorizontalLines):
                self.HorizontalLinesList.append(Line())

    def horizontalLinesUpdate(self):
        center_x = int(self.width/2)
        offset = int(self.howManyVerticalLines/2) - 0.5
        spacing = int(self.width * self.v_spacing)

        x_min = center_x - offset*spacing + self.current_offset_x
        x_max = center_x + offset*spacing + self.current_offset_x
        y_spacing = int(self.h_spacing*self.height)
        for i in range(self.howManyHorizontalLines):
            line_y = (i*y_spacing) - self.current_offset_y
            x1,y1 = self.transform(x_min, line_y)
            x2,y2 = self.transform(x_max, line_y)
            self.HorizontalLinesList[i].points = [x1, y1, x2, y2]

    def on_perspectivePoint_x(self, widget, value):
        # print(f"New X co-ordinate is: {value}")
        pass

    def on_perspectivePoint_y(self, widget, value):
        # print(f"New X co-ordinate is: {value}")
        pass

    def transform(self, x, y):
        # return self.transform_2D(x,y)
        return self.transform_perspective(x,y)

    def transform_2D(self,x, y):
        return int(x),int(y)

    def transform_perspective(self, x, y):
        lin_y = (y*self.perspectivePoint_y)/self.height
        if lin_y > self.perspectivePoint_y:
            lin_y = self.perspectivePoint_y
        diff_x = x- self.perspectivePoint_x
        diff_y = self.perspectivePoint_y - lin_y
        factor_y = diff_y/self.perspectivePoint_y
        factor_y = pow(factor_y, 4)
        transformed_x = self.perspectivePoint_x + factor_y*diff_x
        transformed_y = self.perspectivePoint_y - self.perspectivePoint_y*factor_y
        return int(transformed_x), int(transformed_y)

    def update(self, dt):
        time_factor = dt*60
        self.verticalLinesUpdate()
        self.horizontalLinesUpdate()
        y_spacing = int(self.h_spacing*self.height)
        self.current_offset_y += self.SPEED*time_factor

        if self.current_offset_y >= y_spacing:
            self.current_offset_y -= y_spacing
        # x_spacing = int(self.width * self.v_spacing)
        self.current_offset_x += self.current_speed_x*time_factor

    def on_touch_down(self, touch):
        if touch.x <= self.width /2:
            self.current_speed_x = self.SPEED_X
            print("LEFT")
        else:
            self.current_speed_x = -self.SPEED_X
            print("RIGHT")

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.current_speed_x = 0
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
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

class GalaxyApp(App):
    pass

GalaxyApp().run()