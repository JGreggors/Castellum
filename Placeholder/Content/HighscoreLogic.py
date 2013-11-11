import Zero
import Events
import Property
import VectorMath
import Keys
import io
import NamesNScores

class HighscoreLogic:
    def Initialize(self, initializer):
        self.names = [] #set'in up dem variables
        self.scores = []
        
        self.listedScoreData = []
        
        self.yourFinalScore = Zero.Game.Score.FinalScore
        
        Zero.Connect(Zero.Keyboard, Events.KeyDown, self.OnKeyDown) #get cho buttons ready
       
        for i in range(1,6): #While in the range between 1-5, append the names thus finding the cogs
            self.names.append(self.Space.FindObjectByName("Name" + str(i)))
            self.scores.append(self.Space.FindObjectByName("Score"+ str(i)))
            
        i = 0 # loop counter
        AllText = Zero.OpenText("DefaultHighScore") # Reading from dat TextBlock
        highScores = io.StringIO(AllText.read())    # get dem values
        AllText.close() # close that biatch
        
        for line in highScores:
            currentLine = line.rstrip()
            listingLine = currentLine.split(":")
            self.listedScoreData.append(NamesNScores.NamesNScores(listingLine[0], listingLine[1]))
        
        self.WriteHighScore()
        
    def WriteHighScore(self):
        for i in range(0,5):
            self.names[i].SpriteText.Text = self.listedScoreData[i].name
            self.scores[i].SpriteText.Text = self.listedScoreData[i].score
        
        
    def OnKeyDown(self, KeyboardEvent):
        key = KeyboardEvent.Key
        if(key >= Keys.A and key <= Keys.Z):
            print(key)


Zero.RegisterComponent("HighscoreLogic", HighscoreLogic)