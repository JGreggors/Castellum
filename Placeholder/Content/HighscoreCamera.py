import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vector3

class HighscoreCamera:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.MouseUpdate, self.onMouseUpdate)
        self.CurrentTran = self.Owner.Transform.Translation
        
    def OnLogicUpdate(self, UpdateEvent):
        self.Owner.Transform.Translation = self.CurrentTran
        
    def onMouseUpdate(self, MouseEvent):
        if(MouseEvent.Scroll.y > 0 and not self.Owner.Transform.Translation.y > 0):
            self.CurrentTran.y += 1
        elif(MouseEvent.Scroll.y < 0 and not self.Owner.Transform.Translation.y < -10 and self.Space.CurrentLevel.Name == "Highscore"):
            self.CurrentTran.y += -1
        elif(MouseEvent.Scroll.y < 0 and not self.Owner.Transform.Translation.y < -43 and self.Space.CurrentLevel.Name == "Controls"):
            self.CurrentTran.y += -1
Zero.RegisterComponent("HighscoreCamera", HighscoreCamera)