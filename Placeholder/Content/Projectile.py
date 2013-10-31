import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class Projectile:
    Speed = Property.Float(1.0)
    Direction = Vec3(0,0,0)

    
    def Initialize(self, initializer):

        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Transform.Translation += self.Direction * UpdateEvent.Dt * self.Speed
        
    def OnCollisionStart(self, CollisionEvent):
        otherObject = CollisionEvent.OtherObject
        if(otherObject.Name != "Gold" and otherObject.Name != "Player" and otherObject.Name != "GateAOE" and otherObject.Name != "SwitchGateAOE"):
            self.Owner.Destroy()
        #if(otherObject.Name == "Floor"):
        #    self.Owner.Destroy()
        #if(otherObject.Name == "Bat"):
        #    self.Owner.Destroy()
        #if(otherObject.Name == "Goblin"):
        #    self.Owner.Destroy()
        #if(otherObject.Name == "Gate1"):
        #    self.Owner.Destroy()
        #if(otherObject.Name == "Gate2"):
        #    self.Owner.Destroy()

Zero.RegisterComponent("Projectile", Projectile)