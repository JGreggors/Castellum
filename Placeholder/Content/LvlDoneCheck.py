import Zero
import Events
import Property
import VectorMath
import os

class LvlDoneCheck:
    def Initialize(self, initializer):
        self.UserDirect = Zero.GetUserDirectory()
        self.filename = "save.txt"
        self.Owner.Sprite.Visible = False
        self.Check()
        
    def Check(self):
        self.scores = [[0] * 10 for i in range(10)]
        
        if(os.path.isfile(self.UserDirect + "Castellum\\" + self.filename)):
            ScoreFile = open(self.UserDirect + "Castellum\\" + self.filename, "r")
            
            for i in range(10):
                self.scores[i] = int(ScoreFile.readline())
                print(self.scores[i])
                
            ScoreFile.close()
        
            if(self.Owner.Name == "Check1"):
                if(self.scores[0] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check2"):
                if(self.scores[1] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check3"):
                if(self.scores[2] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check4"):
                if(self.scores[3] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check5"):
                if(self.scores[4] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check6"):
                if(self.scores[5] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check7"):
                if(self.scores[6] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check8"):
                if(self.scores[7] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check9"):
                if(self.scores[8] > 0):
                    self.Owner.Sprite.Visible = True
            elif(self.Owner.Name == "Check10"):
                if(self.scores[9] > 0):
                    self.Owner.Sprite.Visible = True
        

Zero.RegisterComponent("LvlDoneCheck", LvlDoneCheck)