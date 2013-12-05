########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class GoldPickup:
#Logic for gold being destroyed when player collects it
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        
        #if player runs into gem the object is destroyed
        otherObject = CollisionEvent.OtherObject
        if(otherObject.Name == "Player"):
            self.Owner.Destroy()

Zero.RegisterComponent("GoldPickup", GoldPickup)