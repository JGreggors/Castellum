########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Keys
import io
import NamesNScores

class HighscoreLogic:
#For putting high score on high score page
    
    def Initialize(self, initializer):
        
        #setting up arrays for values
        self.names = []
        self.scores = []
        self.listedScoreData = []
        
        #Getting score from score script
        self.yourFinalScore = Zero.Game.Score.FinalScore

       #Append names of objects in high score page
        for i in range(1,12):
            self.names.append(self.Space.FindObjectByName("Name" + str(i)))
            self.scores.append(self.Space.FindObjectByName("Score"+ str(i)))
            
        #Grabs scores from where they are stored
        i = 0
        AllText = Zero.OpenText("DefaultHighScore") 
        highScores = io.StringIO(AllText.read())   
        AllText.close()
        
        #Uses NamesNScores script to append arrays
        for line in highScores:
            currentLine = line.rstrip()
            listingLine = currentLine.split(":")
            self.listedScoreData.append(NamesNScores.NamesNScores(listingLine[0], listingLine[1]))
        
        #runs write high score function
        self.WriteHighScore()
        
    def WriteHighScore(self):
        
        #change the text on high score page
        for i in range(0,10):
            self.names[i].SpriteText.Text = self.listedScoreData[i].name
            self.scores[i].SpriteText.Text = self.listedScoreData[i].score
        


Zero.RegisterComponent("HighscoreLogic", HighscoreLogic)