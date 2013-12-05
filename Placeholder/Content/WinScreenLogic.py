########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class WinScreenLogic:
#Used to tell the game when all levels have been completed and to bring up win screen

    def Initialize(self, initializer):
        
        #Creating an update event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        #setting up checks that wiin screens have been achieved
        self.WinTutorial = False
        self.WinDougMode = False
        self.WinAdventure = False
        self.WinDaredevil = False
        self.WinAll = False

    def OnLogicUpdate(self, UpdateEvent):
        
        #Setting variables to persistant variables from Level Toggle Script
        self.WinTutorial = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinTutorial
        self.WinDougMode = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinDougMode
        self.WinAdventure = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAdventure
        self.WinDaredevil = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinDaredevil
        self.WinAll = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAll
        
    def Check(self):
        
        #basically if all levels are complete load win screen for whole game
        if(self.WinTutorial == True and self.WinDougMode == True and self.WinAdventure == True and self.WinDaredevil == True and self.WinAll == False):
            self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAll = True
            self.Space.LoadLevel("Win5")
            return
        
        #otherwise load Level Select Page
        self.Space.LoadLevel("LevelSelect")
        
Zero.RegisterComponent("WinScreenLogic", WinScreenLogic)