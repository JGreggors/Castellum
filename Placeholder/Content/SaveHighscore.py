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


class SaveHighscore:
#Logic for storing high scores
  
    def Initialize(self, initializer):
        #file where scores are stored
        self.filename = "save.txt"
        #set score after player reaches the end of a level
        self.score = self.Owner.EndLevelLogic.LevelFinalScore
        #check which level the player has finished
        self.LevelNumber = Zero.Game.Score.LevelNumber
        #getting user info for file i/o
        self.UserDirect = Zero.GetUserDirectory()
        #run write file function
        self.WriteFile()
        
    def WriteFile(self):
        
        #if path does not exist create it
        if(not os.path.exists(self.UserDirect + "Castellum")):
            os.mkdir( self.UserDirect + "\\Castellum")
            
        #if file for score does not exist create it and set scores to zero    
        if(not os.path.isfile(self.UserDirect + "Castellum\\" + self.filename)):
            initialScores = "0\n"
            #set to store 11 scores
            for i in range(0,10):
                initialScores += "0\n"
            NameFile = open(self.UserDirect + "Castellum\\" + self.filename, "w")
            NameFile.write(initialScores)
            #close file when done
            NameFile.close()
        
        #run open file function
        self.OpenFile()

    def OpenFile(self):
        
        #varaible for holding scores
        listScores = []
        
        #open file with scores and read in data then close file
        NameFile = open( self.UserDirect + "Castellum\\" + self.filename, "r")
        allText = NameFile.read().splitlines()
        NameFile.close()
        

        #store in array
        for line in allText:
            listScores.append(int(line.rstrip() ))
        
        #---------------------------------------------------
        #Writing new scores achieved by player to file
        newScores = ""
        if(listScores[self.LevelNumber - 1] < self.score):
            listScores[self.LevelNumber - 1] = self.score
        for score in listScores:
            newScores += str(score) + "\n"
        NameFile = open(self.UserDirect + "Castellum\\" + self.filename, "w")
        NameFile.write(newScores)
        NameFile.close()
        #---------------------------------------------------

Zero.RegisterComponent("SaveHighscore", SaveHighscore)