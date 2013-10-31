import Zero
import Events
import Property
import VectorMath

class HUDCreator:
    
    LevelForHUD = Property.Resource("Level")
    
    def Initialize(self, initializer):
        self.HUDSpace = Zero.Game.CreateNamedSpace("HUDSpace", "Space")
        
        self.HUDSpace.LoadLevel(self.LevelForHUD)
        
        
        

Zero.RegisterComponent("HUDCreator", HUDCreator)