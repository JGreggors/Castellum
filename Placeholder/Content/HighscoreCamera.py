########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class HighscoreCamera:
#Setting up Camera logic for high score page
#Same logic also used for controls page

    def Initialize(self, initializer):
        
        #Creating a Logic Update Event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #Creating a Mouse Event
        Zero.Connect(self.Owner, Events.MouseUpdate, self.onMouseUpdate)
        
        #Setting a variable for cameras current translation
        self.CurrentTran = self.Owner.Transform.Translation
        
    def OnLogicUpdate(self, UpdateEvent):
        
        #setting the camera translation to current translation as it updates
        self.Owner.Transform.Translation = self.CurrentTran
        
    def onMouseUpdate(self, MouseEvent):
        
        #Logic for scrolling up
        if(MouseEvent.Scroll.y > 0 and not self.Owner.Transform.Translation.y > 0):
            self.CurrentTran.y += 1
            
        #Logic for scrolling down (Limitations are unique to each level)
        #HighScore Level
        elif(MouseEvent.Scroll.y < 0 and not self.Owner.Transform.Translation.y < -10 and self.Space.CurrentLevel.Name == "Highscore"):
            self.CurrentTran.y += -1
        #Contols Level
        elif(MouseEvent.Scroll.y < 0 and not self.Owner.Transform.Translation.y < -37 and self.Space.CurrentLevel.Name == "Controls"):
            self.CurrentTran.y += -1
            
Zero.RegisterComponent("HighscoreCamera", HighscoreCamera)