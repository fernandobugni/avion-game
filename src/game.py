import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject

import os, sys

from aircraft import *
from map import *
from camera import *
from keyboard import *
from screen import *
from collision import *
from bullet import *
from dynamicObject import *

debug = 0

class World(DirectObject):
    "world class of the game"

    def __init__(self):
        print "Game Starts"
        
        #Load the first environment model
        mydir = os.path.dirname(sys.path[0])
        mydir = Filename.fromOsSpecific(mydir).getFullpath()
        mydirMap = mydir + "/models/scenario/chocolateterrain.egg"
        mydirSky = mydir + "/models/scenario/skysphere.egg.pz"
        mydirStars = mydir + "/models/scenario/stars.jpg"
        #mydir = mydir + "/models/scenario/scene1.egg"
        self.map = map("my map", [0, 0, 0], [0.25, 0.25, 0.25], mydirMap, mydirSky, mydirStars)
                
        #Load aircraft
        mydir = os.path.dirname(sys.path[0])
        mydir = Filename.fromOsSpecific(mydir).getFullpath()
        mydir = mydir + "/models/scifi fighter/alice-scifi--fighter/fighter.egg"
        
        self.aircraft1 = aircraft("fighter1", [0, 0, 20], [0.05, 0.05, 0.05], mydir)    
       
        self.aircraft2 = aircraft("fighter2", [0, 20, 20], [0.05, 0.05, 0.05], mydir)    
        
        self.aircraft1.set_target(self.aircraft2)
        self.aircraft2.set_target(self.aircraft1)
        #load camera
        #base.disableMouse()
        self.camera1 = camera(self.aircraft1.getModel(), "cam1")
        
        self.camera2 = camera(self.aircraft2.getModel(), "cam1")

        #load screen
        self.screen = screen(self.camera1, self.camera2)
        
        #keyboard
        self.keyborad = keyboard(self.aircraft1, self.aircraft2, self.camera1, self.camera2)        
                
        #load collision
        self.collision = collision(self.map, self.aircraft1, self.aircraft2, debug)
                        
        #dynamicObject
        self.objects = dynamicObject(self.collision, self.keyborad, self.aircraft1, self.aircraft2, self.camera1, self.camera2, self.map)
                
        self.aircraft1.setObjects(self.objects)
        self.aircraft2.setObjects(self.objects)
        
        self.aircraft1.setAngleH(0)
        self.aircraft2.setAngleH(180)#0
        
        plight = PointLight('plight')
        plnp = render.attachNewNode(plight)
        plnp.setPos(0, 25, 80)
        render.setLight(plnp)
       
        colour = (0,0,0.4)
        linfog = Fog("A linear-mode Fog node")
        linfog.setMode(Fog.MLinear)
        linfog.setColor(*colour)
        #linfog.setLinearRange(0,320)
        #linfog.setLinearFallback(45,160,320)
        linfog.setExpDensity(0.001)
        a = render.attachNewNode(linfog)
        a.setPos(0,0,20)
        render.setFog(linfog)
        
        #taskMgr.popupControls()
        
        #self.aircraft2.getModel().place()
        
        base.setFrameRateMeter(True)
        
        taskMgr.add(self.main,"Main")
      
    def main(self, task):
        if(debug): print "Loop"
        
        #idea: using MVC pattern 
        self.input()
        self.move()
        
        return Task.cont
        
    def input(self):
        #Use the user events and modify the model
        
        if(debug): 
            print "+input:"
        
        self.keyborad.input()
        
    def move(self):
        #Use the model and modify the screen
        if(debug):
            print "+move:"  
            print self.aircraft1.info()
            print self.aircraft2.info()
            
        #self.aircraft1.move()
        self.aircraft2.move()
        self.camera1.move()
        self.camera2.move()
        
        self.objects.move()
                
        if(debug): 
            print("objects: "+ str(render.ls()) ) 
       
w = World()
run()
