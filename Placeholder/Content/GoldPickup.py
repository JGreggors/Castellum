import Zero
import Events
import Property
import VectorMath

class GoldPickup:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollision)
        
    def OnCollision(self, CollisionEvent):
        #if player runs into me i selfdestruct
        otherObject = CollisionEvent.OtherObject
        if(otherObject.Name == "Player"):
            self.Owner.Destroy()

Zero.RegisterComponent("GoldPickup", GoldPickup)