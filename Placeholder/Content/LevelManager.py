import Zero
import Events
import Property
import VectorMath

class LevelManager:
    
    levelTable = Property.ResourceTable() #which level table
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.GameStarted, self.OnGameStarted)
        
    def OnGameStarted(self, GameEvent):
        self.gameSpace = self.Owner.CreateSpace("GameSpace")
        
        self.gameSpace.LoadLevel(self.levelTable.GetValueAt(0))
        
    def GetCurrentLevelIndex(self):
        return self.levelTable.FindIndexOfResource(self.gameSpace.CurrentLevel)
        
    def GetLevelCount(self):
        return self.levelTable.Size
        
    def LoadNextLevel(self):
        indexOfLevelToLoad = self.GetCurrentLevelIndex()
        
        numberOfLevelInTable = self.GetLevelCount()
        
        if(indexOfLevelToLoad < numberOfLevelInTable - 1):
            indexOfLevelToLoad += 1
            
        levelResourceName = self.levelTable.GetResourceAt(indexOfLevelToLoad)
        
        
        self.gameSpace.LoadLevel(levelResourceName)
        
    def LoadSpecificLevel(self, levelIndex):
        numberOfLevelInTable = self.GetLevelCount()
        print(numberOfLevelInTable)
        if(levelIndex <= numberOfLevelInTable - 1):
            levelResourceName = self.levelTable.GetResourceAt(levelIndex)
            self.gameSpace.LoadLevel(levelResourceName)
            
        

Zero.RegisterComponent("LevelManager", LevelManager)