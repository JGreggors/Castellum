import Zero
import Events
import Property
import VectorMath

class Score:
    tutorial = Property.Bool(True)
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.GameStarted, self.OnGameStarted)
        self.FinalScore = 0
        
    def OnGameStarted(self, GameEvent):
        #pass
        #connects via LevelManager
        self.gameSpace = self.Owner.FindSpaceByName("GameSpace")
        Zero.Connect(self.gameSpace, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        #print(self.FinalScore)
        #If the Player reaches the end
        #print(self.gameSpace)
        End = self.gameSpace.FindObjectByName("End")
        if(End):
            if(End.NextLevel.EndGame == True):
                #store all level statistics for scoring and load next level
                if(self.tutorial == True):
                    Zero.Game.LevelManager.LoadNextLevel()
                else:
                    self.par = self.gameSpace.FindObjectByName("LevelSettings").Timer.par
                    self.finalTime = self.gameSpace.FindObjectByName("LevelSettings").Timer.totalTime
                    self.finalDeaths = self.gameSpace.FindObjectByName("Player").Health.totalDeath
                    self.finalGold = self.gameSpace.FindObjectByName("Player").MasterPlayerContr.gold
                    Zero.Game.FindSpaceByName("HUDSpace").Destroy()
                    Zero.Game.LevelManager.LoadNextLevel()
                

Zero.RegisterComponent("Score", Score)