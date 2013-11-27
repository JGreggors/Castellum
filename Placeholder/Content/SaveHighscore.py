import Zero
import Events
import Property
import VectorMath
import io
import pickle
import os
import Keys


class SaveHighscore:
    def Initialize(self, initializer):
        self.filename = "save.txt"
        self.score = self.Owner.EndLevelLogic.LevelFinalScore
        self.LevelNumber = Zero.Game.Score.LevelNumber
        self.UserDirect = Zero.GetUserDirectory()
        self.WriteFile()
        
    def WriteFile(self):
        if(not os.path.exists(self.UserDirect + "Castellum")):
            os.mkdir( self.UserDirect + "\\Castellum")
            
        if(not os.path.isfile(self.UserDirect + "Castellum\\" + self.filename)):
            initialScores = "0\n"
            
            for i in range(0,9):
                initialScores += "0\n"
            
            
            
            NameFile = open(self.UserDirect + "Castellum\\" + self.filename, "w")
            NameFile.write(initialScores)
            
            NameFile.close()
        
        self.OpenFile()

            
    def OpenFile(self):
        listScores = []
        NameFile = open( self.UserDirect + "Castellum\\" + self.filename, "r")
        
        allText = NameFile.read().splitlines()
        NameFile.close()
        

        
        for line in allText:
            #print("LINE:  " + line)
            #line.rstrip() 
            #print("[" + line + "]")
            #test = []
            #for char in line.rstrip():
            #    test.append(char)
            
            #print("TEST: " + test)
            
            listScores.append(int(line.rstrip() ))
            
            #print("[" + str(listScores[0]) + "]")
        
        newScores = ""
        if(listScores[self.LevelNumber - 1] < self.score):
            listScores[self.LevelNumber - 1] = self.score
        for score in listScores:
            newScores += str(score) + "\n"
        print(newScores)
        NameFile = open(self.UserDirect + "Castellum\\" + self.filename, "w")
        NameFile.write(newScores)
        NameFile.close()

Zero.RegisterComponent("SaveHighscore", SaveHighscore)