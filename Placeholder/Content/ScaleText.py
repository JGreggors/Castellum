########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class ScaleText:
#This is the logic for having text get big and small in game
    
    def Initialize(self, initializer):
        
        #Creating Update Event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        #Setting variable to see when the text needs to get big
        self.big = True

    def OnLogicUpdate(self, UpdateEvent):
        
        #to make the text big scale object and it's boxcollider
        if(self.big):
            self.Owner.Transform.Scale += VectorMath.Vec3(.006, .006, 0)
            if(self.Owner.BoxCollider):
                self.Owner.BoxCollider.Size += VectorMath.Vec3(.006, .006, 0)
            if(self.Owner.Transform.Scale.x > 1.4):
                self.big = False
                
        #if it has reached the biggest size set start to shrink
        else:
            self.Owner.Transform.Scale -= VectorMath.Vec3(.006, .006, 0)
            if(self.Owner.BoxCollider):
                self.Owner.BoxCollider.Size -= VectorMath.Vec3(.006, .006, 0)
            if(self.Owner.Transform.Scale.x < 1):
                self.big = True
                

Zero.RegisterComponent("ScaleText", ScaleText)