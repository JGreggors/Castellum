import Zero
import Events
import Property
import VectorMath

class MusicLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.backgroundMusicObject = self.Space.FindObjectByName("BackgroundMusic")
        
        if(self.backgroundMusicObject):
            self.backgroundMusicObject.Persistent = True
            
        if(not self.backgroundMusicObject):
            self.backgroundMusicObject = self.Space.Create("BackgroundMusic")
            self.backgroundMusicObject.Persistent = True
            
        if(self.backgroundMusicObject.SoundEmitter.IsPlaying() == False):
            self.backgroundMusicObject.SoundEmitter.Play()
            
    def OnLogicUpdate(self, UpdateEvent):
        #if(Zero.Keyboard.KeyIsPressed(Zero.Keys.M)):
            #print("M")
            #self.Space.SoundSpace.Pause = not self.Space.SoundSpace.Pause
            
            
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.Shift)):
            self.Space.ReloadLevel()

Zero.RegisterComponent("MusicLogic", MusicLogic)