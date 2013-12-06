########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

#Creating shortcut for VectorMath.Vec3
Vec3 = VectorMath.Vec3

class RespawnKey:
    def Initialize(self, initializer):
        
        #Creating a Collision Event
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
        #Creating variable for starting place of key
        self.keySpawn = self.Owner.Parent.Transform.Translation
        
    def OnCollisionStart(self, CollisionEvent):
        
        #short cuts for key objects
        key = self.Owner.Parent.Transform.Translation
        aoe = self.Owner.Transform.Translation
        
        #if the key falls into the fire pit
        if(CollisionEvent.OtherObject.Name == "Pit"):
            #Create fizzle effect
            self.Space.CreateAtPosition("FizzleKey", Vec3(key.x, key.y + 1, key.z))
            #Set key back to original position in level
            self.Owner.Parent.Transform.Translation = self.keySpawn
            #play fizzle sound effect
            self.Space.SoundSpace.PlayCue("fizzle")
            

Zero.RegisterComponent("RespawnKey", RespawnKey)