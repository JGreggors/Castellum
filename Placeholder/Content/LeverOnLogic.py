import Zero
import Events
import Property
import VectorMath

class LeverOnLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
    def OnCollisionStart(self, CollisionEvent):
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            self.Space.SoundSpace.PlayCue("opengate")
            self.Owner.FindChildByName("Lever").Sprite.SpriteSource = "leveron"

Zero.RegisterComponent("LeverOnLogic", LeverOnLogic)