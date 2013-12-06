########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import pickle
import io
import os
import Keys

class LoadHighscore:
#Logic for reading high scores from file

    def Initialize(self, initializer):
        
        #file where scores are stored
        self.filename = "save.txt"
        #getting User info for file i/o
        self.UserDirect = Zero.GetUserDirectory()
        #run open file function
        self.OpenFile()
        
    def OpenFile(self):
        #creating arrays to store scores
        scores = []
        listScores = []
        
        #if file exists open it and read in scores
        if(os.path.isfile(self.UserDirect + "Castellum\\" + self.filename)):
            NameFile = open( self.UserDirect + "Castellum\\" + self.filename, "r")
            allText = NameFile.read().splitlines()
            NameFile.close()
            

            #store in array
            for line in allText:
                listScores.append(line.rstrip())
                
            #edit the scores to the scores stored in file
            for i in range(1,12):
                scores.append(self.Space.FindObjectByName("Score"+ str(i)))
                scores[i - 1].SpriteText.Text = listScores[i - 1]
                

Zero.RegisterComponent("LoadHighscore", LoadHighscore)