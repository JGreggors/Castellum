########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Property
import math
import Color

class Timer:
#Logic for HUD timer
    
    #setting changeable variable for level par
    par = Property.Float(180.0)
    
    def Initialize(self, initializer):
        
        #Creating Update Event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        #initializing total time to zero
        self.totalTime = 0.0
        
        #for setting and update timer
        self.secondsPassed = 0
        self.starttime = self.secondsPassed
        self.timertext = self.Owner.HUDCreator.HUDSpace.FindObjectByName("Timer")
        
    def OnLogicUpdate(self, UpdateEvent):

        #updating seconds pass and total time
        self.secondsPassed += UpdateEvent.Dt
        self.totalTime += UpdateEvent.Dt

       #----------------------------------------------------------------------------
       #Finding the HUD if there is one and updating the timer text object
        hudSpace = Zero.Game.FindSpaceByName("HUDSpace")
        if(not hudSpace):
            pass
        timeObject = hudSpace.FindObjectByName("Timer")
        if(timeObject):
            timeObject.SpriteText.Text = str(round(self.secondsPassed, 1))
       #----------------------------------------------------------------------------
        
        #If players time goes over the par set for that letter the timer text turns red
        if(self.totalTime > self.par):
            self.timertext.SpriteText.Color = Color.Red

Zero.RegisterComponent("Timer", Timer)