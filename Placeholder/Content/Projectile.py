########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

#Creating shortcut for Vector3
Vec3 = VectorMath.Vec3

class Projectile:
#Logic for projectile from weapon
    
    #Varaibles
    Speed = Property.Float(1.0)
    Direction = Vec3(0,0,0)
    timedDestruction = Property.Float(3.5)

    
    def Initialize(self, initializer):
        
        #creating update and collision events
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        #setting variables
        self.existanceTimer = 0
        
    def OnLogicUpdate(self, UpdateEvent):
        
        #Moving logic
        self.Owner.Transform.Translation += self.Direction * UpdateEvent.Dt * self.Speed
        #increase timer
        self.existanceTimer += UpdateEvent.Dt * 10
        #destroy after a certain time
        if(self.existanceTimer > self.timedDestruction):
            self.Owner.Destroy()
        
    def OnCollisionStart(self, CollisionEvent):
        #if the projectile collides with anything except the player, keys, gold, or gates it is destroyed
        otherObject = CollisionEvent.OtherObject
        if(otherObject.Name != "Player" and otherObject.Name != "Key" and otherObject.Name != "AOE" and otherObject.Name != "Gold" and otherObject.Name != "GateAOE" and otherObject.Name != "SwitchGateAOE"):
            self.Owner.Destroy()


Zero.RegisterComponent("Projectile", Projectile)