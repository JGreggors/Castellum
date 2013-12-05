########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import os

class GlobalVolume:
#Setting up logic for volume control in game
    
    def Initialize(self, initializer):
        
        #Checks if there is a volume text file and creates one if it doesn't exist
        if os.path.exists(Zero.GetUserDirectory() + "Castellum") and os.path.isfile(Zero.GetUserDirectory() + "Castellum\\volume_options.txt"):
            
            #opens file for reading
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'r+')
            #reads in value after converting it to an integer
            self.percent = int(self.file.readline())
            #closes file
            self.file.close()
         
        elif os.path.exists(Zero.GetUserDirectory() + "Castellum"):
            
            #opens file for writing
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'w')
            #writes to fiile 100 (max volume)
            self.file.write("100")
            #closes file
            self.file.close()
            #re-Intitializes script so we can check to read file
            self.Initialize(initializer)
            
        else: 
            
            #Creating a file if there wasn't one
            os.mkdir(Zero.GetUserDirectory() + "Castellum")
            self.file = open(Zero.GetUserDirectory() + "Castellum" + "volume_options.txt", 'w')
            #writes to file 100 (max Volume)
            self.file.write("100")
            #Closes file
            self.file.close()
            #re-Intitializes script so we can check to read file
            self.Initialize(initializer)
        
        #Set of Logic Update Event
        Zero.Connect(self.Space, Events.LogicUpdate, self.onLogicUpdate)
        
        #Set variable for whether volume is trying to be changed
        self.changeVolume = False
        
    def onLogicUpdate(self, UpdateEvent):
        
        #if the volume is being changed by player
        if(self.changeVolume):
            
            #run this function
            self.setVolume()
            #then reset variable since volume has been changed
            self.changeVolume = False
        
    def setVolume(self):
        
        #Reads the text file (we already checked that it exists) as an integer and then closes file
        self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'r+')
        self.volume = int(self.file.readline())
        self.file.close()
        
        #changes the volume in the SoundEmitter for object playing background music
        self.backgroundMusicObject = self.Space.FindObjectByName("BackgroundMusic")
        self.backgroundMusicObject.SoundEmitter.Volume = self.volume / 100
        #also changes volume in soundspace for other sounds
        self.Space.SoundSpace.Volume = self.volume / 100.0

Zero.RegisterComponent("GlobalVolume", GlobalVolume)