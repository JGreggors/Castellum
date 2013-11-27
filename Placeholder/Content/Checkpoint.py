import Zero
import Events
import Property
import VectorMath
import Color

class Checkpoint:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.visible = False
        
    def OnLogicUpdate(self, UpdateEvent):
        text = self.Owner.FindChildByName("CheckpointText").SpriteText
        if(self.visible == True):
            text.Color.a += 0.01
            if(text.Color.a >= 1):
                text.Color.a = 1
                self.visible = False
        if(self.visible == False and text.Color.a >= 0):
            text.Color.a += -0.01
            if(text.Color.a <= 0):
                text.Color.a = 0
                
        print(text.Color.a)
        
    def OnCollisionStart(self, CollisionEvent):
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.visible = True
            self.Space.FindObjectByName("Player").Health.StartPlace = self.Space.FindObjectByName("Player").Transform.Translation
            self.Space.SoundSpace.PlayCue("menu")
Zero.RegisterComponent("Checkpoint", Checkpoint)