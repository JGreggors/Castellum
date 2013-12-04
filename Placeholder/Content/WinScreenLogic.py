import Zero
import Events
import Property
import VectorMath

class WinScreenLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #setting up checks that wiin screens have been achieved
        self.WinTutorial = False
        self.WinDougMode = False
        self.WinAdventure = False
        self.WinDaredevil = False
        self.WinAll = False

    def OnLogicUpdate(self, UpdateEvent):
        
        self.WinTutorial = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinTutorial
        self.WinDougMode = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinDougMode
        self.WinAdventure = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAdventure
        self.WinDaredevil = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinDaredevil
        self.WinAll = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAll
        
    def Check(self):
        if(self.WinTutorial == True and self.WinDougMode == True and self.WinAdventure == True and self.WinDaredevil == True and self.WinAll == False):
            self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAll = True
            #basically if all levels are complete load win screen for whole game
            self.Space.LoadLevel("Win5")
            return
        
        self.Space.LoadLevel("LevelSelect")
        
Zero.RegisterComponent("WinScreenLogic", WinScreenLogic)