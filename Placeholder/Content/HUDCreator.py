import Zero
import Events
import Property
import VectorMath

class HUDCreator:
    
    LevelForHUD = Property.Resource("Level")
    
    def Initialize(self, initializer):
        self.HUDSpace = Zero.Game.CreateNamedSpace("HUDSpace", "Space")
        
        self.HUDSpace.LoadLevel(self.LevelForHUD)
       
        self.BGSpace = Zero.Game.CreateNamedSpace("BGSpace", "Space")
        
        self.BGSpace.LoadLevel("Background")
        
    def Destroyed(self):
        
        self.BGSpace.Destroy()
        

Zero.RegisterComponent("HUDCreator", HUDCreator)