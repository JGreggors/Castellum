########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class Fizzle:
#Creating a fizzle effect for when player/keys falls into fire pit
    
    alphaTimer = Property.Float(0.001)
    destroyTimer = Property.Int(75)
    
    def Initialize(self, initializer):
        #Creating an Update Event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
            
    def OnLogicUpdate(self, UpdateEvent):
        #Editing color of particle effect and destroying it after a certain time
        self.Owner.SpriteParticleSystem.Tint = self.Owner.SpriteParticleSystem.Tint - VectorMath.Vec4(0, 0, 0, self.alphaTimer)
        self.destroyTimer -= 1
        if(self.destroyTimer == 0):
            self.Owner.Destroy()

Zero.RegisterComponent("Fizzle", Fizzle)