########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Color

class countdown:
#Logic for numbers generated when enemy is stunned

    #Variables
    alphaTimer = Property.Float(0.01)
    destroyTimer = Property.Int(50)
    upSpeed = Property.Float(0.5)
    
    def Initialize(self, initializer):
        
        #creating Update event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
            
    def OnLogicUpdate(self, UpdateEvent):

        #number bounces above enemy and then is destroyed afterwards
        self.Owner.Transform.Translation.y += self.upSpeed * UpdateEvent.Dt
        self.Owner.SpriteText.Color = self.Owner.SpriteText.Color - VectorMath.Vec4(0, 0, 0, self.alphaTimer)
        self.destroyTimer -= 1
        if(self.destroyTimer == 0):
            self.Owner.Destroy()

Zero.RegisterComponent("countdown", countdown)