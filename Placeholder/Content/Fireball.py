import Zero
import Events
import Property
import VectorMath

class Fireball:
    Dropdistance = Property.Float(0.0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if(self.Owner.Transform.Translation.y < -15):
            self.Owner.Transform.Translation = VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y+18.6, self.Owner.Transform.Translation.z)

Zero.RegisterComponent("Fireball", Fireball)