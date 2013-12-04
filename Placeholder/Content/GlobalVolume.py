import Zero
import Events
import Property
import VectorMath
import os

class GlobalVolume:
    def Initialize(self, initializer):
        #Checks if there is a volume text file and creates one if it doesn't exist
        if os.path.exists(Zero.GetUserDirectory() + "Castellum") and os.path.isfile(Zero.GetUserDirectory() + "Castellum\\volume_options.txt"):
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'r+')
            self.percent = int(self.file.readline())
            self.file.close()
        elif os.path.exists(Zero.GetUserDirectory() + "Castellum"):
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'w')
            self.file.write("100")
            self.file.close()
            self.Initialize(initializer)
        else: 
            os.mkdir(Zero.GetUserDirectory() + "Castellum")
            self.file = open(Zero.GetUserDirectory() + "Castellum" + "volume_options.txt", 'w')
            self.file.write("100")
            self.file.close()
            self.Initialize(initializer)
        
        Zero.Connect(self.Space, Events.LogicUpdate, self.onLogicUpdate)
        self.changeVolume = False
        
    def onLogicUpdate(self, UpdateEvent):
        #Changes the volume if it needs to
        if(self.changeVolume):
            self.setVolume()
            self.changeVolume = False
        
    def setVolume(self):
        #Reads the text file (we already checked that it exists) and sets the global volume to what is read
        self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'r+')
        self.volume = int(self.file.readline())
        self.file.close()
        self.backgroundMusicObject = self.Space.FindObjectByName("BackgroundMusic")
        self.backgroundMusicObject.SoundEmitter.Volume = self.volume / 100
        self.Space.SoundSpace.Volume = self.volume / 100.0

Zero.RegisterComponent("GlobalVolume", GlobalVolume)