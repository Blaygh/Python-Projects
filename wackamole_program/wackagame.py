'''Wackagame app'''

# ensure Kivy window is not resizable (must be done before any other kivy imports)
from kivy.config import Config
Config.set('graphics', 'resizable', False)

# import all necessary Kivy modules
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from time import perf_counter
import random

# game constants
FONT_NAME = 'Bahnschrift'
CENTER_FONT_COLOR = 0,0,0,1
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FLOOR = 58
TOP = 200
MIDDLE = 350
RIGHT = 650
LEFT = 50
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 150
ENEMY_WIDTH = 100
ENEMY_HEIGHT = 100



# collision detection function
def collision(r1pos,r1size,r2pos,r2size):
    # is r1 left of r2?
    if r1pos[0]+r1size[0]<r2pos[0]:
        return False
    # is r1 right of r2?
    if r1pos[0]>r2pos[0]+r2size[0]:
        return False
    # is r1 below r2?
    if r1pos[1]+r1size[1]<r2pos[1]:
        return False
    # is r1 above r2?
    if r1pos[1]>r2pos[1]+r2size[1]:
        return False
    # otherwise, they are colliding
    return True



# Wackagame App
class Wackagame(App,):
    def build(self):
        # creat root Widget with canvas, rectangles on canvas
        root = Widget()
        with root.canvas:
            #/////////////////////Creating basic game objects 5 holes and mole object and background///////
            #BACKGROUND
            Rectangle(source='wackaland.png',pos=(0,0),size=(WINDOW_WIDTH,WINDOW_HEIGHT))
            #TOP LEFT
            self.hole1 = Rectangle(source='wackahole.png',pos=(RIGHT - 120,TOP), size=(ENEMY_WIDTH,ENEMY_HEIGHT))
            # TOP RIGHT
            self.hole5 = Rectangle(source='wackahole.png',pos=(LEFT + 120,TOP), size=(ENEMY_WIDTH,ENEMY_HEIGHT))
            # TOP LEFT
            self.hole2 = Rectangle(source='wackahole.png',pos=(LEFT,FLOOR), size=(ENEMY_WIDTH,ENEMY_HEIGHT))
            # MIDDLE
            self.hole3 = Rectangle(source='wackahole.png',pos=(MIDDLE,FLOOR), size=(ENEMY_WIDTH,ENEMY_HEIGHT))
            # BOTTOM LEFT
            self.hole4 = Rectangle(source='wackahole.png',pos=(RIGHT,FLOOR), size=(ENEMY_WIDTH,ENEMY_HEIGHT))
            # MOLE
            self.player = Rectangle(source='wackamole.png',pos=(WINDOW_WIDTH/2-PLAYER_WIDTH/2,FLOOR), size=(PLAYER_WIDTH,PLAYER_HEIGHT))


        # add score label to root
        self.scoreLabel = Label(font_size=24,font_name=FONT_NAME,valign='top',halign='left',padding=(20,20),size=(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.scoreLabel.text_size = self.scoreLabel.size # or, if label size might change, you can use self.label.bind(size=self.label.setter('text_size'))
        root.add_widget(self.scoreLabel)

        self.timeElapse = Label(font_size=24,font_name=FONT_NAME,valign='top',halign='center',padding=(20,20),size=(WINDOW_WIDTH,WINDOW_HEIGHT))
        self.scoreLabel.text_size = self.scoreLabel.size
        root.add_widget(self.timeElapse)

        # add center-screen label to root, with instructions to start game
        self.centerLabel = Label(text='Press space to start...',font_size=48,font_name=FONT_NAME,color=CENTER_FONT_COLOR,markup=True,halign='center',size=(WINDOW_WIDTH,WINDOW_HEIGHT))
        root.add_widget(self.centerLabel)

        #bind keyboard
        self._keyboard = Window.request_keyboard(lambda:None, root)
        self._keyboard.bind(on_key_down=self.onKeyDown)

        # bind mouse events to the root widget
        root.bind(on_touch_down=self.on_mouse_down)
        root.bind(on_touch_up=self.on_mouse_up)

        # get the mouse object, listen for touchdown event
        #self.bind(on_press = self.on_touch_down,on_key_up=self.on_touch_up)

        # set running flag to False
        self.running = False
        # return root widget
        return root
    
    def startGame(self):
        self.centerLabel.text = ''
        self.setScore(0)
        self.startTime = perf_counter()
        self.hole1.source = 'wackahole.png'
        Clock.schedule_interval(self.update,1)
        Clock.schedule_interval(self.updatetime,0.01) #printing time elpased since game start
        Clock.schedule_interval(self.on_mouse_down,2)

        self.running = True
    
    def randomPop(self):
        '''randomly select the which hole to pop up from'''
        self.posList = [self.hole1.pos,self.hole2.pos,self.hole3.pos,self.hole4.pos,self.hole5.pos]
        return random.choice(self.posList)
        

    def update(self,okay):
        self.player.pos = self.randomPop()
        
#TODO print time elapsed
    def updatetime(self,counter):
         endTime = float(perf_counter())
         self.runningTime =  endTime - self.startTime
         self.timeElapse.text = f'Time: {self.runningTime: 0.2f}'


#print score on the screen
    def setScore(self,score):
            self.score = score
            self.scoreLabel.text = f'Score: {self.score}'
            self.timeElapse.text = f'Time: {perf_counter()}'
            


    # def _keyboard_closed(self):
    #     self._mouse.unbind(on_key_down=self.onKeyDown,on_key_up=self.onKeyUp)
    #     self._mouse = None

    def onKeyDown(self, keyboard, keycode, text, modifiers):

        if keycode[1]=='spacebar':
            self.startGame()

    def on_mouse_down(self,spos,*args):
        if self.running:
            print(args)
            # loop through each molehole rectangle, check if it collides with the mouse click/touch pos
            if collision(self.player.pos, self.player.size, args, (1,1)):
                self.setScore(self.score + 1)


    def on_mouse_up(self, pos,button):
        pass


Window.size = (WINDOW_WIDTH,WINDOW_HEIGHT)
Wackagame().run()
