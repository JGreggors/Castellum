########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class LeverOnLogic:
    def Initialize(self, initializer):
        #Creating collision event
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
    def OnCollisionStart(self, CollisionEvent):
        
        #if projectile hits lever
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            #play sound effect
            self.Space.SoundSpace.PlayCue("opengate")
            #switch sprite to animate sprite
            self.Owner.FindChildByName("Lever").Sprite.SpriteSource = "leveron"

Zero.RegisterComponent("LeverOnLogic", LeverOnLogic)