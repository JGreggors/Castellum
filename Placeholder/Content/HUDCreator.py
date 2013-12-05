########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class HUDCreator:
#Creating Spaces for HUD and  game gackground
    
    #Setting a variable so we can set which level is used as a HUD
    LevelForHUD = Property.Resource("Level")
    
    def Initialize(self, initializer):
        
        #Creating a Space for the HUD
        self.HUDSpace = Zero.Game.CreateNamedSpace("HUDSpace", "Space")
        #Load specified level into this Space
        self.HUDSpace.LoadLevel(self.LevelForHUD)
       
       
        #creating a Space for the Backgrounf
        self.BGSpace = Zero.Game.CreateNamedSpace("BGSpace", "Space")
        #Load level containing background
        self.BGSpace.LoadLevel("Background")
        
    def Destroyed(self):
        
        #will destroy Background space when level is destroyed
        self.BGSpace.Destroy()
        
Zero.RegisterComponent("HUDCreator", HUDCreator)