import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class Projectile:
    Speed = Property.Float(1.0)
    Direction = Vec3(0,0,0)
    timedDestruction = Property.Float(3.5)

    
    def Initialize(self, initializer):

        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        self.existanceTimer = 0
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Transform.Translation += self.Direction * UpdateEvent.Dt * self.Speed
        self.existanceTimer += UpdateEvent.Dt * 10
        if(self.existanceTimer > self.timedDestruction):
            self.Owner.Destroy()
        
    def OnCollisionStart(self, CollisionEvent):
        otherObject = CollisionEvent.OtherObject
        if(otherObject.Name != "Player" and (otherObject.Name == "Key" and otherObject.Name == "AOE" and otherObject.Name != "Gold" and otherObject.Name != "GateAOE" and otherObject.Name != "SwitchGateAOE" and otherObject.Name != "FadeIn" and otherObject.Name != "FadeOut")):
            self.Owner.Destroy()


Zero.RegisterComponent("Projectile", Projectile)