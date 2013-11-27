import Zero
import Events
import Property
import VectorMath
import Property
import Keys
import Zero
import Events
import Property
import VectorMath
import Property
import Keys

class EndLevelLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        
        self.levelProgression = 0.0 #This is the timer for adding the score
        self.startTimeScore = 0 #This sets beginning score from time to 0
        self.startGoldScore = 0 #This sets beginning score from Gold to 0
        self.startDeathScore = 0 #This sets beginning score from deaths to 0
        
        self.timeIsDone = False
        self.goldIsDone = False
        
        self.getStats = False #Should I get stats immediately?
        self.endLevel = False # Should I end level?
        
        self.LevelFinalScore = 0 #your total score for the level
        
        #Get you final time and level par from last level
        self.finalTime = Zero.Game.Score.finalTime
        self.par = Zero.Game.Score.par
        
        #Get final deaths from last level
        self.finalDeaths = Zero.Game.Score.finalDeaths
        
        #Get final gold from last level
        self.finalGold = Zero.Game.Score.finalGold
       #--------------------------------------------------------
        
        #Calculate time score
        self.tscore = (round(self.par - self.finalTime)) * 5
        #Calculate gold score
        self.tgold = self.finalGold * 5
        #Calculate Death score
        self.tdeath = self.finalDeaths * 20
        
        self.LevelFinalScore = self.tscore + self.tgold - self.tdeath
        self.Owner.AddComponentByName("SaveHighscore")
        
    def OnLogicUpdate(self, UpdateEvent):
        #If Space is pressed Add up score
        if(Zero.Keyboard.KeyIsPressed(Keys.Space)):
            self.getStats = True
        if(Zero.Keyboard.KeyIsPressed(Keys.N)):
            self.Space.LoadLevel("MainMenu")
        if(Zero.Keyboard.KeyIsPressed(Keys.B)):
            self.Space.LoadLevel("EndSlide")

            
       #--------------------------------------------------------
        #Start timer
        self.levelProgression += UpdateEvent.Dt
        

       #--------------------------------------------------------
        #This is the spritetext that prints your time score
        clock = self.Space.FindObjectByName("tTime").SpriteText
        #This is the spritetext that prints your gold score
        gold = self.Space.FindObjectByName("tGold").SpriteText
        #This is the spritetext that prints your death score
        deaths = self.Space.FindObjectByName("tDeaths").SpriteText
        #This is the spritetext that prints your total score
        total = self.Space.FindObjectByName("tTotal").SpriteText
       #---------------------------------------------------------
        #If true
        if(self.getStats):
            #Print out stats immediately
            clock.Text = str(round(self.tscore))
            gold.Text = str(round(self.tgold))
            deaths.Text = str(round(-self.tdeath))
            total.Text = str(round(self.tscore + self.tgold - self.tdeath))
            #if you press Space again end level
            if((Zero.Keyboard.KeyIsPressed(Keys.Space) and self.endLevel) or (self.timeIsDone == True and self.goldIsDone == True)):
                Zero.Game.LevelManager.LoadNextLevel()
                
            self.endLevel = True
        
        #Otherwise
        else:
            #Slowly add up time score
            if(self.levelProgression > 1 and self.startTimeScore <= self.tscore):
                self.startTimeScore += 1 * (UpdateEvent.Dt * 100000)
                clock.Text = str(round(self.startTimeScore))
            if(self.startTimeScore >= self.tscore):
                clock.Text = str(round(self.tscore))
                self.timeIsDone = True
            #Slowly add up gold score
            if(self.levelProgression > 2 and self.startGoldScore <= self.tgold):
                if(self.finalGold == 0):
                    gold.Text = "0"
                    self.goldIsDone = True
                else:
                    self.startGoldScore += 1 * (UpdateEvent.Dt * 1000)
                    gold.Text = str(round(self.startGoldScore))
                    if(self.startGoldScore >= self.tgold):
                        gold.Text = str(round(self.tgold))
                        self.goldIsDone = True
            #slowly add up death score
            if(self.levelProgression > 3 and self.startDeathScore <= self.tdeath):
                if(self.finalDeaths == 0):
                    deaths.Text = "0"
                else:
                    self.startDeathScore += 1 * (UpdateEvent.Dt * 100)
                    deaths.Text = str(round(-self.startDeathScore))
            #add up total
            if(self.timeIsDone == True and self.goldIsDone == True):
                total.Text = str(round(self.tscore + self.tgold - self.tdeath))

Zero.RegisterComponent("EndLevelLogic", EndLevelLogic)