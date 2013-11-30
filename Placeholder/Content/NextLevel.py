import Zero
import Events
import Property
import VectorMath

class NextLevel:
    LevelNumber = Property.Int(0)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        self.EndGame = False
    def OnCollisionStart(self, CollisionEvent):
        
        
        otherObject = CollisionEvent.OtherObject
        if(otherObject.Name == "Player"):
            Zero.Game.Score.LevelNumber = self.LevelNumber
            self.EndGame = True
            #self.Space.LoadLevel("EndLevel")
        

            

Zero.RegisterComponent("NextLevel", NextLevel)