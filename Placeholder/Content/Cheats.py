########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

#Making a shortcut for VectorMath.Vec3
Vec3 = VectorMath.Vec3

class Cheats:
#Logic for Cheats in order to quickly progress through levels
#for presentations, testing purposes and proof of win screens

    def Initialize(self, initializer):
        #Setting up a Keyboard Event
        Zero.Connect(Zero.Keyboard, Events.KeyDown, self.OnKeyDown)
        
    def OnKeyDown(self, KeyboardEvent):
        
        #Defining player to a variable
        player = self.Space.FindObjectByName("Player")
        
        #if Zero is pressed the character will be moved to a translation by the level exit
        #translation is set for each individual level
        if(KeyboardEvent.Key == Zero.Keys.Zero):
            
            #Level1 - Tutorial
            if(self.Space.CurrentLevel.Name == "IzzyLevel1"):
                player.Transform.Translation = Vec3(120.5, -.01, 0)
            #Level2 - Tutorial
            elif(self.Space.CurrentLevel.Name == "IzzyLevel5"):
                player.Transform.Translation = Vec3(-46.547, -2.38, 0)
            
            #Level 3 - Doug Mode
            elif(self.Space.CurrentLevel.Name == "IzzyLevel2"):
                player.Transform.Translation = Vec3(56.666,-9.355, 0)
            #Level 4 - Doug Mode
            elif(self.Space.CurrentLevel.Name == "JG1"):
                player.Transform.Translation = Vec3(82.701, -0.302, 0)
            #Level 5 - Doug Mode
            elif(self.Space.CurrentLevel.Name == "IzzyLevel3"):
                player.Transform.Translation = Vec3(41.606, -8.36, 0)
            
            #Level 6 - Adventure
            elif(self.Space.CurrentLevel.Name == "IzzyLevel4"):
                player.Transform.Translation = Vec3(95.917, -8.35, 0)
            #Level 7 - Adventure
            elif(self.Space.CurrentLevel.Name == "JG2"):
                player.Transform.Translation = Vec3(86.06, -0.429, 0)
            #Level 8 - Adventure
            elif(self.Space.CurrentLevel.Name == "IzzyLevel7"):
                player.Transform.Translation = Vec3(41.591, -8.11, 0)
            
            
            #Level 9 - Daredevil
            elif(self.Space.CurrentLevel.Name == "IzzyLevel8"):
                player.Transform.Translation = Vec3(95.877, -9.331, 0)
            #Level 10 - Daredevil
            elif(self.Space.CurrentLevel.Name == "IzzyLevel6"):
                player.Transform.Translation = Vec3(34.468, 2.704, 0)
            #Level 11 - Daredevil
            elif(self.Space.CurrentLevel.Name == "IzzyLevel9"):
                player.Transform.Translation = Vec3(62.763, -1.318, 0)

Zero.RegisterComponent("Cheats", Cheats)