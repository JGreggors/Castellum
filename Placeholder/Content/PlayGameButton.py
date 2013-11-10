import Zero
import Events
import Property
import VectorMath

class PlayGameButton:
    def Initialize(self, initializer):
        #takes event update from UIButton
        Zero.Connect(self.Owner, "ClickedUIButton", self.OnClickedUIButton)
        
    def OnClickedUIButton(self, ClickedUIButtonEvent):
        #Basically if object is called " " go to " " level
        #can change as needed 
        if(self.Owner.Name == "Start"):
            self.Space.LoadLevel("InfiniteGrap")
            
        elif(self.Owner.Name == "LevelSelect"):
            self.Space.LoadLevel("Level")
            
        elif(self.Owner.Name == "Credits"):
            self.Space.LoadLevel("SampleLevel")

Zero.RegisterComponent("PlayGameButton", PlayGameButton)