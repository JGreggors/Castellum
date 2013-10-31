import Zero
import Events
import Property
import VectorMath
import Color

class Death:
    alphaTimer = Property.Float(0.001)
    destroyTimer = Property.Int(1000)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
            
    def OnLogicUpdate(self, UpdateEvent):
        #print(self.destroyTimer)
        #print(self.Owner.Sprite.Color)
        self.Owner.Sprite.Color = self.Owner.Sprite.Color - VectorMath.Vec4(0, 0, 0, self.alphaTimer)
        self.destroyTimer -= 1
        if(self.destroyTimer == 0):
            self.Owner.Destroy()

Zero.RegisterComponent("Death", Death)