########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class LevelManager:
    
    #resource table property
    levelTable = Property.ResourceTable() 
    
    def Initialize(self, initializer):
        
        #Checking for when game starts
        Zero.Connect(self.Owner, Events.GameStarted, self.OnGameStarted)
        
    def OnGameStarted(self, GameEvent):
        
        #Get a reference to the game space
        self.gameSpace = self.Owner.CreateSpace("GameSpace")
        #load the first level in the level table
        self.gameSpace.LoadLevel(self.levelTable.GetValueAt(0))
        
    def GetCurrentLevelIndex(self):
        #returns the current level's index in the level table
        return self.levelTable.FindIndexOfResource(self.gameSpace.CurrentLevel)
        
    def GetLevelCount(self):
        #returns the level count
        return self.levelTable.Size
        
    def LoadNextLevel(self):
        
        #index of level to load
        indexOfLevelToLoad = self.GetCurrentLevelIndex()
        #number of levels in the level table
        numberOfLevelInTable = self.GetLevelCount()
        #bounds checking
        if(indexOfLevelToLoad < numberOfLevelInTable - 1):
            indexOfLevelToLoad += 1
        #get name of level resource at provided index
        levelResourceName = self.levelTable.GetResourceAt(indexOfLevelToLoad)
        #load next level
        self.gameSpace.LoadLevel(levelResourceName)
        
    def LoadSpecificLevel(self, levelIndex):
        #Logic to load a specific level when called
        
        #number of levels in the level table
        numberOfLevelInTable = self.GetLevelCount()
        #if it is a valid level index
        if(levelIndex <= numberOfLevelInTable - 1):
            #get name of level resource at provided index
            levelResourceName = self.levelTable.GetResourceAt(levelIndex)
            #load that level
            self.gameSpace.LoadLevel(levelResourceName)
            
Zero.RegisterComponent("LevelManager", LevelManager)