import Zero
import Events
import Property
import VectorMath

class MusicLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.P)):
            self.Space.SoundSpace.Pause = not self.Space.SoundSpace.Pause

Zero.RegisterComponent("MusicLogic", MusicLogic)