import Zero
import Events
import Property
import VectorMath

class Score:
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.GameStarted, self.OnGameStarted)
        
    def OnGameStarted(self, GameEvent):
        #pass
        #connects via LevelManager
        self.gameSpace = self.Owner.FindSpaceByName("GameSpace")
        Zero.Connect(self.gameSpace, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        #If the Player reaches the end
        #print(self.gameSpace)
        End = self.gameSpace.FindObjectByName("End")
        if(End):
            if(End.NextLevel.EndGame == True):
                #store all level statistics for scoring and load next level
                self.par = self.gameSpace.FindObjectByName("LevelSettings").Timer.par
                self.finalTime = self.gameSpace.FindObjectByName("LevelSettings").Timer.totalTime
                self.finalDeaths = self.gameSpace.FindObjectByName("Player").Health.totalDeath
                self.finalGold = self.gameSpace.FindObjectByName("Player").MasterPlayerContr.gold
                Zero.Game.LevelManager.LoadNextLevel()
                

Zero.RegisterComponent("Score", Score)