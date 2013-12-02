import Zero
import Events
import Property
import VectorMath

class ScaleText:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.big = True
        
    def OnLogicUpdate(self, UpdateEvent):
        if(self.big):
            self.Owner.Transform.Scale += VectorMath.Vec3(.006, .006, 0)
            if(self.Owner.Transform.Scale.x > 1.4):
                self.big = False
        else:
            self.Owner.Transform.Scale -= VectorMath.Vec3(.006, .006, 0)
            if(self.Owner.Transform.Scale.x < 1):
                self.big = True
                

Zero.RegisterComponent("ScaleText", ScaleText)