import Zero
import Events
import Property
import VectorMath
import os

class LevelToggles:
    def Initialize(self, initializer):
        #------------------------------------------------------
        #for file i/o for checking game progress
        self.UserDirect = Zero.GetUserDirectory()
        self.filename = "save.txt"
        
        
        #setting up an array to hold score values
        self.scores = [[0] * 10 for i in range(10)]
        #checking if this path exists
        if(os.path.isfile(self.UserDirect + "Castellum\\" + self.filename)):
            #opens file
            ScoreFile = open(self.UserDirect + "Castellum\\" + self.filename, "r")
            #reads in scores stores in file
            for i in range(10):
                #changes scores to integers
                self.scores[i] = int(ScoreFile.readline())
                
            #Close file    
            ScoreFile.close()
        else:
            for i in range(10):
                #changes scores to integers
                self.scores[i] = 0
            
         
        if(self.scores[0] > 0 and self.scores[1] > 0 and self.scores[2] > 0):
            self.WinTutorial = True
        else:
            self.WinTutorial = False
            
        if(self.scores[3] > 0 and self.scores[4] > 0 and self.scores[5] > 0):    
            self.WinDougMode = True
        else:
            self.WinDougMode = False
            
        if(self.scores[6] > 0 and self.scores[7] > 0 and self.scores[8] > 0):
            self.WinAdventure = True
        else:
            self.WinAdventure = False
            
        if(self.scores[9] > 0):
            self.WinDaredevil = True
        else:
            self.WinDaredevil = False
            
        self.WinAll = False
        
        self.Owner.Persistent = True
        

Zero.RegisterComponent("LevelToggles", LevelToggles)