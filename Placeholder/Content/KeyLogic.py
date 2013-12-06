########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath


class KeyLogic:
    def Initialize(self, initializer):
        
        #Creating a collision event
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
        #saving the starting placement of a key in a level
        self.StartLocation = self.Space.FindObjectByName("Key").Transform.Translation
        
    def OnCollisionStart(self, CollisionEvent):
        
        #if the key falls into a fire pit, create fizzle effect and put it back at start location
        if(CollisionEvent.OtherObject.Name == "Pit"):
            self.Space.CreateAtPosition("FizzleKey", VectorMath.Vec3(self.Space.FindObjectByName("Key").Transform.Translation))
            self.Space.FindObjectByName("Key").Transform.Translation = self.StartLocation
            

Zero.RegisterComponent("KeyLogic", KeyLogic)