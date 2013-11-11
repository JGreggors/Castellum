import Zero
import Events
import Property
import VectorMath

class KeyLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        self.StartLocation = self.Space.FindObjectByName("Key").Transform.Translation
        
    def OnCollisionStart(self, CollisionEvent):
        if(CollisionEvent.OtherObject.Name == "Pit"):
            self.Space.CreateAtPosition("FizzleKey", VectorMath.Vec3(self.Space.FindObjectByName("Key").Transform.Translation))
            self.Space.FindObjectByName("Key").Transform.Translation = self.StartLocation
            

Zero.RegisterComponent("KeyLogic", KeyLogic)