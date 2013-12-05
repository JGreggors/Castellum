########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class MusicLogic:
#Logic for a persistant object to play music throughout game
    
    def Initialize(self, initializer):
        
        #defining object to play music
        self.backgroundMusicObject = self.Space.FindObjectByName("BackgroundMusic")
        
        #if the object exists make it persistant
        if(self.backgroundMusicObject):
            self.backgroundMusicObject.Persistent = True
        
        #if it doesn't exist create one and make it persistant
        if(not self.backgroundMusicObject):
            self.backgroundMusicObject = self.Space.Create("BackgroundMusic")
            self.backgroundMusicObject.Persistent = True
            
        #if the music isn't playing set it so it is playing
        if(self.backgroundMusicObject.SoundEmitter.IsPlaying() == False):
            self.backgroundMusicObject.SoundEmitter.Play()

Zero.RegisterComponent("MusicLogic", MusicLogic)