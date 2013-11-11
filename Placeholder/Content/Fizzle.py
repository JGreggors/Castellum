import Zero
import Events
import Property
import VectorMath

class Fizzle:
    alphaTimer = Property.Float(0.001)
    destroyTimer = Property.Int(75)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
            
    def OnLogicUpdate(self, UpdateEvent):
        print(self.destroyTimer)
        #print(self.Owner.Sprite.Color)
        self.Owner.SpriteParticleSystem.Tint = self.Owner.SpriteParticleSystem.Tint - VectorMath.Vec4(0, 0, 0, self.alphaTimer)
        self.destroyTimer -= 1
        if(self.destroyTimer == 0):
            self.Owner.Destroy()

Zero.RegisterComponent("Fizzle", Fizzle)