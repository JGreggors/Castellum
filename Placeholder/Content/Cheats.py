import Zero
import Events
import Property
import VectorMath
Vec3 = VectorMath.Vec3
class Cheats:
    def Initialize(self, initializer):
        Zero.Connect(Zero.Keyboard, Events.KeyDown, self.OnKeyDown)
        
    def OnKeyDown(self, KeyboardEvent):
        player = self.Space.FindObjectByName("Player")
        if(KeyboardEvent.Key == Zero.Keys.Zero):
            if(self.Space.CurrentLevel.Name == "Level2"):
                player.Transform.Translation = Vec3(26, -1, 0)
            elif(self.Space.CurrentLevel.Name == "Level3"):
                player.Transform.Translation = Vec3(72, 33, 0)
            elif(self.Space.CurrentLevel.Name == "Level4"):
                player.Transform.Translation = Vec3(112, -1, 0)
            elif(self.Space.CurrentLevel.Name == "InfiniteGrap"):
                player.Transform.Translation = Vec3(63.5, -5, 0)
            
        
        

Zero.RegisterComponent("Cheats", Cheats)