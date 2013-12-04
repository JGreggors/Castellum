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
            if(self.Space.CurrentLevel.Name == "IzzyLevel1"):
                player.Transform.Translation = Vec3(120.5, -.01, 0)
            
            elif(self.Space.CurrentLevel.Name == "IzzyLevel5"):
                player.Transform.Translation = Vec3(-46.547, -2.38, 0)
            
            elif(self.Space.CurrentLevel.Name == "IzzyLevel2"):
                player.Transform.Translation = Vec3(56.666,-9.355, 0)
            
            elif(self.Space.CurrentLevel.Name == "JG1"):
                player.Transform.Translation = Vec3(82.701, -0.302, 0)
            
            elif(self.Space.CurrentLevel.Name == "IzzyLevel3"):
                player.Transform.Translation = Vec3(41.606, -8.36, 0)
            
            elif(self.Space.CurrentLevel.Name == "IzzyLevel4"):
                player.Transform.Translation = Vec3(95.917, -8.35, 0)
            
            elif(self.Space.CurrentLevel.Name == "JG2"):
                player.Transform.Translation = Vec3(86.06, -0.429, 0)
            
            elif(self.Space.CurrentLevel.Name == "IzzyLevel7"):
                player.Transform.Translation = Vec3(41.591, -8.11, 0)
            
            elif(self.Space.CurrentLevel.Name == "IzzyLevel8"):
                player.Transform.Translation = Vec3(95.877, -9.331, 0)
            
            elif(self.Space.CurrentLevel.Name == "IzzyLevel6"):
                player.Transform.Translation = Vec3(34.468, 2.704, 0)
            
            elif(self.Space.CurrentLevel.Name == "IzzyLevel9"):
                player.Transform.Translation = Vec3(62.763, -1.318, 0)

        
        

Zero.RegisterComponent("Cheats", Cheats)