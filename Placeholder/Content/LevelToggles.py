########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import os

class LevelToggles:
#Checks whether win screens should be loaded
#Makes sure win screens will only be displayed once

    def Initialize(self, initializer):
        
        #for file i/o for checking game progress
        self.UserDirect = Zero.GetUserDirectory()
        self.filename = "save.txt"
        
        
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
        else:
            for i in range(11):
                #changes scores to integers
                self.scores[i] = 0
            
        #sets if a win screen should be played based on whether scores have been stored
        #Win Screen for Tutorials
        if(self.scores[0] > 0 and self.scores[1] > 0):
            self.WinTutorial = True
        else:
            self.WinTutorial = False
            
        #Win Screen for Doug Mode
        if(self.scores[2] > 0 and self.scores[3] > 0 and self.scores[4] > 0):    
            self.WinDougMode = True
        else:
            self.WinDougMode = False
            
        #Win Screen for Adventure
        if(self.scores[5] > 0 and self.scores[6] > 0 and self.scores[7] > 0):
            self.WinAdventure = True
        else:
            self.WinAdventure = False
            
        #Win Screen for Daredevil
        if(self.scores[8] > 0 and self.scores[9] > 0 and self.scores[10] > 0):
            self.WinDaredevil = True
        else:
            self.WinDaredevil = False
            
        #Win screen for entire game
        self.WinAll = False
        
        #makes object persistant throughtout game
        self.Owner.Persistent = True
        

Zero.RegisterComponent("LevelToggles", LevelToggles)