import Zero
import Events
import Property
import VectorMath

class Checkpoint:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
    def OnCollisionStart(self, CollisionEvent):
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.Space.FindObjectByName("Player").Health.StartPlace = self.Space.FindObjectByName("Player").Transform.Translation
            self.Space.SoundSpace.PlayCue("menu")

Zero.RegisterComponent("Checkpoint", Checkpoint)