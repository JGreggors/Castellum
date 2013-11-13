import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class RespawnKey:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
        self.keySpawn = self.Owner.Parent.Transform.Translation
        
    def OnCollisionStart(self, CollisionEvent):
        key = self.Owner.Parent.Transform.Translation
        aoe = self.Owner.Transform.Translation
        if(CollisionEvent.OtherObject.Name == "Pit"):
            self.Space.CreateAtPosition("FizzleKey", Vec3(key.x, key.y + 1, key.z))
            self.Owner.Parent.Transform.Translation = self.keySpawn
            self.Space.SoundSpace.PlayCue("fizzle")
            

Zero.RegisterComponent("RespawnKey", RespawnKey)