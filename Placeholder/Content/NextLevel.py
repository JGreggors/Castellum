import Zero
import Events
import Property
import VectorMath

class NextLevel:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        self.EndGame = False
    def OnCollisionStart(self, CollisionEvent):
        otherObject = CollisionEvent.OtherObject
        if(otherObject.Name == "Player"):
            self.EndGame = True
            #self.Space.LoadLevel("EndLevel")

Zero.RegisterComponent("NextLevel", NextLevel)