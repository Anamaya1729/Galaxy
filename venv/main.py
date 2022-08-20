from kivy.config import Config
Config.set("graphics","width",1100)
Config.set("graphics","height",700)
from kivy.uix.relativelayout import RelativeLayout
from kivy import platform
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line,Quad, Triangle
from kivy.metrics import sp
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.lang.builder import Builder
import random

Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from User_actions import on_keyboard_up,on_keyboard_down,on_touch_up,on_touch_down,keyboard_closed
    menu_widget = ObjectProperty()
    menu_title = StringProperty("G   A   L   A   X   Y")
    button_title = StringProperty("START")
    perspectivePoint_x = NumericProperty(0)
    perspectivePoint_y = NumericProperty(0)
    Score = StringProperty("Score : 0")
    howManyVerticalLines = 18
    v_spacing = .34# Percentage in screen width
    VerticalLinesList = []

    howManyHorizontalLines = 12
    h_spacing = .14 #Percentage in screen height
    HorizontalLinesList = []

    current_offset_y = 0
    current_loop_y = 0

    SPEED = 1
    SPEED_X = 5
    current_speed_x = 0
    current_offset_x = 0

    howManyTiles = 16
    TilesList = []
    TilesCoordinates = []

    ship_coordinates = [(0, 0), (0, 0), (0, 0)]
    Ship = None
    Ship_width = .2
    Ship_base_y = .05
    ship_height = .12

    GAME_OVER = False
    GAME_STARTED = False

    begin_Sound= None
    galaxy_Sound = None
    gameover_Sound = None
    gameover_Voice= None 
    Music1 = None
    restart_Sound = None

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.Sound_Loader()
        self.initVerticalLines()
        self.initHorizontalLines()
        self.initTiles()
        self.game_reset()
        self.initShip()
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up = self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def Sound_Loader(self):
        self.begin_Sound = SoundLoader.load("audio/begin.wav")
        self.galaxy_Sound = SoundLoader.load("audio/galaxy.wav")
        self.gameover_Sound = SoundLoader.load("audio/gameover_impact.wav")
        self.gameover_Voice = SoundLoader.load("audio/gameover_voice.wav")
        self.Music1 = SoundLoader.load("./audio/Music2.mp3")
        self.restart_Sound = SoundLoader.load("audio/restart.wav")

        #self.Music1.volume = .7
        #self.gameover_Sound.volume = .6
        #self.gameover_Voice.volume = .25
        #self.restart_Sound.volume = .25
        #self.begin_Sound.volume = .25


    def game_reset(self):
        self.SPEED = 1
        self.current_loop_y = 0
        self.current_offset_y = 0
        self.current_offset_x = 0 
        self.current_speed_x = 0
        self.TilesCoordinates = []
        self.pre_fill_tiles_coordinates()
        self.generate_tile_coordinate()
        self.GAME_OVER = False

    def initShip(self):
        with self.canvas:
            Color(0,0,0)
            self.ship = Triangle()
    
    def Ship_update(self):
        center_x = self.width/2
        ship_base = self.Ship_base_y* self.height
        ship_height = self.ship_height* self.height
        Ship_width = self.Ship_width * self.width
        ship_half_width = Ship_width/2

        self.ship_coordinates[0] = (center_x - ship_half_width,ship_base)
        self.ship_coordinates[1] = (center_x,ship_height)
        self.ship_coordinates[2] = (center_x+ ship_half_width,ship_base)
        x1,y1 = self.Transform(*self.ship_coordinates[0])
        x2,y2 = self.Transform(*self.ship_coordinates[1])
        x3,y3=  self.Transform(*self.ship_coordinates[2])
        self.ship.points = [x1,y1,x2,y2,x3,y3]
 
    def check_ship_collsision(self):
        for i in range(len(self.TilesCoordinates)):
            ti_x, ti_y = self.TilesCoordinates[i]
            if ti_y > self.current_loop_y + 1:
                return False
            if self.check_ship_collision_with_tiles(ti_x,ti_y):
                return True
        return False

    def check_ship_collision_with_tiles(self,ti_x,ti_y):
        xmin, ymin = self.get_tile_coordinate(ti_x,ti_y)
        xmax, ymax = self.get_tile_coordinate(ti_x+1,ti_y+1)
        for i in range(3):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False
    
    def on_game_start_press(self):
        print("Start??")
        #if self.GAME_OVER:
         #   self.restart_Sound.play()
        #else:
         #   self.begin_Sound.play()
        #self.Music1.play()
        self.game_reset()
        self.GAME_STARTED = True
        self.menu_widget.opacity= 0

    def play_game_music(self,dt):
        #self.Music1.play()
        pass

    def is_desktop(self):
        if platform in ("linux","win", "macosx"):
            return True
        return False

    def pre_fill_tiles_coordinates(self):
        for i in range(10):
            self.TilesCoordinates.append((0,i))

    def initVerticalLines(self):
        with self.canvas:
            Color(1,1,1)
            for _ in range(self.howManyVerticalLines):
                self.VerticalLinesList.append(Line())
    
    def initTiles(self):
        with self.canvas:
            Color(1,1,1)
            for _ in range(self.howManyTiles):
                self.TilesList.append(Quad())
    
    def get_line_x_from_index(self,index):
        center_line_x = self.perspectivePoint_x
        offset = index - 0.5
        spacing = int(self.width * self.v_spacing)
        line_x = center_line_x + offset* spacing + self.current_offset_x
        return line_x

    def verticalLinesUpdate(self):
        start_index = -int(self.howManyVerticalLines/2) + 1 
        for i in range(start_index,start_index + self.howManyVerticalLines):
            line_x = self.get_line_x_from_index(i)
            x1,y1 = self.Transform(line_x, 0)
            x2,y2 = self.Transform(line_x,self.height)
            self.VerticalLinesList[i].points = [x1, y1, x2, y2]
    
    def initHorizontalLines(self):
        with self.canvas:
            Color(1,1,1)
            for _ in range(self.howManyHorizontalLines):
                self.HorizontalLinesList.append(Line())

    def get_line_y_from_index(self, index):
        y_spacing = int(self.height*self.h_spacing)
        line_y = index*y_spacing - self.current_offset_y
        return line_y

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

    def Transform(self, x, y):
        #return self.transform_2D(x,y)
        return self.transform_perspective(x,y)

    def generate_tile_coordinate(self):
        last_x = 0
        last_y = 0

        if len(self.TilesCoordinates)> 0:
            last_coordinate = self.TilesCoordinates[-1] 
            last_x = last_coordinate[0]
            last_y = last_coordinate[1] + 1

        for i in range(len(self.TilesCoordinates)-1,-1,-1):
            if self.TilesCoordinates[i][1] < self.current_loop_y:
                del self.TilesCoordinates[i]

        for i in range(len(self.TilesCoordinates),self.howManyTiles):
            r = random.randint(0,2)
            start_index = -int(self.howManyVerticalLines/2) + 1
            end_index = start_index+self.howManyVerticalLines - 2
            if last_x<= start_index:
                r = 1
            if last_x >= end_index:
                r = 2
            self.TilesCoordinates.append((last_x,last_y))
            # 0 == straight 1 = right 2 = left

            if r == 1:
                last_x+= 1
                self.TilesCoordinates.append(((last_x,last_y)))
                last_y+= 1
                self.TilesCoordinates.append(((last_x,last_y)))
            if r == 2:
                last_x -= 1
                self.TilesCoordinates.append(((last_x,last_y)))
                last_y +=1
                self.TilesCoordinates.append(((last_x,last_y)))
            last_y += 1

    def Speed_Up(self):
        if self.current_loop_y > 50:
            self.SPEED = 1.5
        if self.current_loop_y > 100:
            self.SPEED = 2
        if self.current_loop_y > 200:
            self.SPEED = 3
        if self.current_loop_y > 300:
            self.SPEED = 4

    def get_tile_coordinate(self, ti_x, ti_y):
        ti_y = ti_y - self.current_loop_y
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def horizontalLinesUpdate(self):
        start_index = -int(self.howManyVerticalLines/2) + 1
        end_index = start_index+self.howManyVerticalLines - 1
        x_min = self.get_line_x_from_index(start_index)
        x_max = self.get_line_x_from_index(end_index)
        for i in range(self.howManyHorizontalLines):
            line_y = self.get_line_y_from_index(i)
            x1,y1 = self.Transform(x_min, line_y)
            x2,y2 = self.Transform(x_max, line_y)
            self.HorizontalLinesList[i].points = [x1, y1, x2, y2]

    def tilesUpdate(self):
        for i in range(self.howManyTiles):
            tile = self.TilesList[i]
            TilesCoordinates = self.TilesCoordinates[i]
            xmin, ymin = self.get_tile_coordinate(TilesCoordinates[0],TilesCoordinates[1])
            xmax, ymax = self.get_tile_coordinate(TilesCoordinates[0]+1,TilesCoordinates[1]+1)
            x1,y1 = self.Transform(xmin,ymin)
            x2,y2 = self.Transform(xmin,ymax)
            x3,y3 = self.Transform(xmax,ymax)
            x4,y4 = self.Transform(xmax,ymin)
            tile.points = [x1,y1, x2, y2, x3,y3, x4, y4]

    def update(self, dt):
        time_factor = dt*60
        self.verticalLinesUpdate()
        self.horizontalLinesUpdate()
        self.tilesUpdate()
        self.Ship_update()
        self.Speed_Up()
        if not self.GAME_OVER and self.GAME_STARTED:
            y_speed = self.SPEED * self.height /100
            y_spacing = int(self.h_spacing*self.height)
            self.current_offset_y += y_speed*time_factor
            x_speed = self.current_speed_x* self.width/100
            while self.current_offset_y >= y_spacing:
                self.current_offset_y -= y_spacing
                self.current_loop_y += 1
                self.Score = f"Score: {self.current_loop_y}"
                self.generate_tile_coordinate()
            x_spacing = int(self.width * self.v_spacing)
            self.current_offset_x += x_speed*time_factor
        if not self.check_ship_collsision() and not self.GAME_OVER:
            self.GAME_OVER = True
            #self.Music1.stop()
            #self.gameover_Sound.play()
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.button_title = "RESTART"
            self.menu_widget.opacity = 1
            print("GAME OVER!")
            Clock.schedule_once(self.play_gameover_voice, 3)
    
    def play_gameover_voice(self, dt):
        if self.GAME_OVER:
            #self.gameover_Voice.play()
            pass

if __name__ == "__main__":
    class GalaxyApp(App):
        pass

    GalaxyApp().run()
