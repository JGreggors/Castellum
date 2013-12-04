import Zero
import Events
import Property
import VectorMath

class MusicLogic:
    def Initialize(self, initializer):
        
        self.backgroundMusicObject = self.Space.FindObjectByName("BackgroundMusic")
        
        if(self.backgroundMusicObject):
            self.backgroundMusicObject.Persistent = True
            
        if(not self.backgroundMusicObject):
            self.backgroundMusicObject = self.Space.Create("BackgroundMusic")
            self.backgroundMusicObject.Persistent = True
            
        if(self.backgroundMusicObject.SoundEmitter.IsPlaying() == False):
            self.backgroundMusicObject.SoundEmitter.Play()
            

Zero.RegisterComponent("MusicLogic", MusicLogic)