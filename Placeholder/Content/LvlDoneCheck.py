########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import os

class LvlDoneCheck:
#Logic for having check sprites appear when a level is completed

    def Initialize(self, initializer):
        
        #for file i/o for checking game progress
        self.UserDirect = Zero.GetUserDirectory()
        self.filename = "save.txt"
        
        #starts check marks as invisible
        self.Owner.Sprite.Visible = False
        #runs check function
        self.Check()
        
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
        
#-----------------------------------------------------------------------------------
#Sets check sprite to visible if a level has been completed (a score was stored)
        
            #Level 1
            if(self.Owner.Name == "Check1"):
                if(self.scores[0] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 2
            elif(self.Owner.Name == "Check2"):
                if(self.scores[1] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 3
            elif(self.Owner.Name == "Check3"):
                if(self.scores[2] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 4
            elif(self.Owner.Name == "Check4"):
                if(self.scores[3] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 5
            elif(self.Owner.Name == "Check5"):
                if(self.scores[4] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 6
            elif(self.Owner.Name == "Check6"):
                if(self.scores[5] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 7
            elif(self.Owner.Name == "Check7"):
                if(self.scores[6] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 8
            elif(self.Owner.Name == "Check8"):
                if(self.scores[7] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 9
            elif(self.Owner.Name == "Check9"):
                if(self.scores[8] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 10
            elif(self.Owner.Name == "Check10"):
                if(self.scores[9] > 0):
                    self.Owner.Sprite.Visible = True
            #Level 11
            elif(self.Owner.Name == "Check11"):
                if(self.scores[10] > 0):
                    self.Owner.Sprite.Visible = True
#-----------------------------------------------------------------------------------

Zero.RegisterComponent("LvlDoneCheck", LvlDoneCheck)