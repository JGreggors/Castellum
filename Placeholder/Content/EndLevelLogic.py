import Zero
import Events
import Property
import VectorMath
import Property
import Keys
import os

class EndLevelLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        
        self.levelProgression = 0.0 #This is the timer for adding the score
        self.startTimeScore = 0 #This sets beginning score from time to 0
        self.startGoldScore = 0 #This sets beginning score from Gold to 0
        self.startDeathScore = 0 #This sets beginning score from deaths to 0
        
        #for live calculating of score
        self.deathsAreDone = False
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
        if(self.finalTime < self.par):
            self.tscore = (round(self.par - self.finalTime)) * 100
        else:
            self.tscore = 0
        #Calculate gold score
        self.tgold = self.finalGold * 200
        #Calculate Death score
        self.tdeath = self.finalDeaths * 100
        #calculate final score
        self.LevelFinalScore = self.tscore + self.tgold - self.tdeath
        self.Owner.AddComponentByName("SaveHighscore")
        
        #------------------------------------------------------
        #for file i/o for checking game progress
        self.UserDirect = Zero.GetUserDirectory()
        self.filename = "save.txt"
        #------------------------------------------------------
        #setting up checks that wiin screens have been achieved
        self.WinTutorial = False
        self.WinDougMode = False
        self.WinAdventure = False
        self.WinDaredevil = False
        self.WinAll = False
        
    def OnLogicUpdate(self, UpdateEvent):
        #If Space is pressed Add up score
        if(Zero.Keyboard.KeyIsPressed(Keys.Space)):
            self.getStats = True

        self.WinTutorial = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinTutorial
        self.WinDougMode = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinDougMode
        self.WinAdventure = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAdventure
        self.WinDaredevil = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinDaredevil
        self.WinAll = self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAll
        
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
                self.Check()
                
                
            self.endLevel = True
        
        #Otherwise
        else:
            #Slowly add up time score
            if(self.levelProgression > 1 and self.startTimeScore <= self.tscore):
                self.startTimeScore += 10 * (UpdateEvent.Dt * 100)
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
                    self.startGoldScore += 10 * (UpdateEvent.Dt * 100)
                    gold.Text = str(round(self.startGoldScore))
                    if(self.startGoldScore >= self.tgold):
                        gold.Text = str(round(self.tgold))
                        self.goldIsDone = True
            #slowly add up death score
            if(self.levelProgression > 3 and self.startDeathScore <= self.tdeath):
                if(self.finalDeaths == 0):
                    deaths.Text = "0"
                    self.deathsAreDone = True
                else:
                    self.startDeathScore += 10 * (UpdateEvent.Dt * 100)
                    deaths.Text = str(round(-self.startDeathScore))
                    self.deathsAreDone = True
            #add up total
            if(self.timeIsDone == True and self.goldIsDone == True and self.deathsAreDone == True):
                total.Text = str(round(self.tscore + self.tgold - self.tdeath))

    def Check(self):
        #setting up an array to hold score values
        self.scores = [[0] * 11 for i in range(11)]
        #checking if this path exists
        if(os.path.isfile(self.UserDirect + "Castellum\\" + self.filename)):
            #opens file
            ScoreFile = open(self.UserDirect + "Castellum\\" + self.filename, "r")
            #reads in scores stores in file
            for i in range(11):
                #changes scores to integers
                self.scores[i] = int(ScoreFile.readline())
                
            #Close file    
            ScoreFile.close()
        #checks current level and if scores have been stored    
        if(self.Space.CurrentLevel.Name == "EndLevel" and self.WinTutorial == False):    
            if(self.scores[0] > 0 and self.scores[1] > 0):
                #if the scores are stored then those levels are complete load win screen
                self.Space.FindObjectByName("LvlToggles").LevelToggles.WinTutorial = True #state this win screen has been achieved
                self.Space.LoadLevel("Win1")
                return
                
        if(self.Space.CurrentLevel.Name == "EndLevel1" and self.WinDougMode == False):
            if(self.scores[2] > 0 and self.scores[3] > 0 and self.scores[4] > 0):
                #if the scores are stored then those levels are complete load win screen
                self.Space.FindObjectByName("LvlToggles").LevelToggles.WinDougMode = True 
                self.Space.LoadLevel("Win2")
                return
                
        if(self.Space.CurrentLevel.Name == "EndLevel2" and self.WinAdventure == False):
            if(self.scores[5] > 0 and self.scores[6] > 0 and self.scores[7] > 0):
                self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAdventure = True 
                #if the scores are stored then those levels are complete load win screen
                self.Space.LoadLevel("Win3")
                return
                
        if(self.Space.CurrentLevel.Name == "EndLevel3" and self.WinDaredevil == False):
            if(self.scores[8] > 0 and self.scores[9] > 0 and self.scores[10] > 0):
                self.Space.FindObjectByName("LvlToggles").LevelToggles.WinDaredevil = True
                #if the scores are stored then those levels are complete load win screen
                self.Space.LoadLevel("Win4")
                return
                
        #if(self.WinTutorial == True and self.WinDougMode == True and self.WinAdventure == True and self.WinDaredevil == True and self.WinAll == False):
        #    self.Space.FindObjectByName("LvlToggles").LevelToggles.WinAll = True
        #    #basically if all levels are complete load win screen for whole game
        #    self.Space.LoadLevel("Win5")
        #    return
        
        self.Space.LoadLevel("LevelSelect")

Zero.RegisterComponent("EndLevelLogic", EndLevelLogic)