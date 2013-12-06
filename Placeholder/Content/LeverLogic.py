########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Color

class LeverLogic:
#Logic for lever to open gates
    
    #is the switch on
    access = False 
    
    def Initialize(self, initializer):
        
        #Creating Collision and Update Events
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        #Setting variables for gate
        self.Switchgate1 = self.Space.FindObjectByName("SwitchGate1")
        self.Switchgate2 = self.Space.FindObjectByName("SwitchGate2")
        
        #storing position of gates
        self.startGate1 = self.Switchgate1.Transform.Translation
        self.startGate2 = self.Switchgate2.Transform.Translation
        
        #variable for changing y coordinate
        self.yAxis = 0.0 
        
    def OnLogicUpdate(self, UpdateEvent):
        
        # If open gates move
        if(self.access == True):
            #increase the y coordinate
            self.yAxis += UpdateEvent.Dt
            #move one gate up and one gate down
            self.Switchgate2.Transform.Translation = self.startGate2 + VectorMath.Vec3(0, -self.yAxis, 0)
            self.Switchgate1.Transform.Translation = self.startGate1 + VectorMath.Vec3(0, self.yAxis, 0)
            #Until max then set doors there
            if(self.yAxis > 3):
                self.yAxis += 0
                self.startGate1 = self.Switchgate1.Transform.Translation
                self.startGate2 = self.Switchgate2.Transform.Translation
        
        #Limit for gate raising
        if(self.yAxis > 3):
            self.access = False
        
        
    def OnCollisionStart(self, CollisionEvent):
        
        otherObject = CollisionEvent.OtherObject
        #if it gets shot initiate
        if(otherObject.Name == "Projectile"):
            self.access = True
            self.Owner.BoxCollider.SendsEvents = False

Zero.RegisterComponent("LeverLogic", LeverLogic)