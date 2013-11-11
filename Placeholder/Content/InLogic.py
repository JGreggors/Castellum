import Zero
import Events
import Property
import VectorMath
import Color

class InLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.startFadeIn = False
        
    def OnLogicUpdate(self, UpdateEvent):
        text = self.Owner.FindRoot().SpriteText
        if(self.startFadeIn == True):
            if(text.Color.w + 0.01 >= 1):
                text.Color.w = 1
            else:
                text.Color.w += 0.005
                
    def OnCollisionStart(self, CollisionEvent):
        player = CollisionEvent.OtherObject.Name == "Player"
        
        if(player):
            self.startFadeIn == True
            

Zero.RegisterComponent("InLogic", InLogic)