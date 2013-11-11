import Zero
import Events
import Property
import VectorMath
import Color

class OutLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.startFadeOut = False
        
    def OnLogicUpdate(self, UpdateEvent):
        text = self.Owner.Parent
        if(self.startFadeOut == True):
            if(text.SpriteText.Color.a - 0.01 <= 0):
                text.SpriteText.Color.a = 0
                print("weeee")
            else:
                text.SpriteText.Color.a -= VectorMath.Vec4(0,0,0,0.005)
                print("wooo")
        print(text.SpriteText.Color.a)
        
    def OnCollisionStart(self, CollisionEvent):
        player = CollisionEvent.OtherObject.Name == "Player"
        
        if(player):
            self.startFadeOut == True
            print("AWWWW SHIT")
            
Zero.RegisterComponent("OutLogic", OutLogic)