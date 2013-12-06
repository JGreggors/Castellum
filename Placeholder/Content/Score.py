########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class Score:
#Grabs all necessary information for score
    
    #used during playtesting for turning score off for tutorials
    #set by ScoreOn and ScoreOff scripts
    tutorial = Property.Bool(True) 
    
    def Initialize(self, initializer):
        
        #checking when the game starts
        Zero.Connect(self.Owner, Events.GameStarted, self.OnGameStarted)
        #Setting up array to hold scores
        self.listOfScores = [0] * 11
        #creating a variabe fore the level number
        self.LevelNumber = 0
        
        
    def OnGameStarted(self, GameEvent):
        #creating a new space
        #connects via LevelManager
        self.gameSpace = self.Owner.FindSpaceByName("GameSpace")
        #creating update event
        Zero.Connect(self.gameSpace, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        #making varaible for object that will store scoes
        End = self.gameSpace.FindObjectByName("End")
        if(End):
            #if the end of a level is reached
            if(End.NextLevel.EndGame == True):
                #store all level statistics for scoring and load next level
                if(self.tutorial == True): 
                    #for when scoring is off
                    Zero.Game.LevelManager.LoadNextLevel()
                else:
                    #stores par, final level time, total deaths, and gems collected
                    self.par = self.gameSpace.FindObjectByName("LevelSettings").Timer.par
                    self.finalTime = self.gameSpace.FindObjectByName("LevelSettings").Timer.totalTime
                    self.finalDeaths = self.gameSpace.FindObjectByName("Player").Health.totalDeath
                    self.finalGold = self.gameSpace.FindObjectByName("Player").MasterPlayerContr.gold
                    #Destroys the HUDSpace
                    Zero.Game.FindSpaceByName("HUDSpace").Destroy()
                    Zero.Game.LevelManager.LoadNextLevel()
                

Zero.RegisterComponent("Score", Score)