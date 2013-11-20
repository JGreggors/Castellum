import Zero
import Events
import Property
import VectorMath
import Keys
import Action
import math
Vec2 = VectorMath.Vec2
Vec3 = VectorMath.Vec3
Vec4 = VectorMath.Vec4
Quat = VectorMath.Quat

class GlobalTime:
    def Initialize(self, init):
        Zero.Connect(Zero.Keyboard, Events.KeyDown, self.OnKeyDown)
        self.Pause = False
    def OnKeyDown(self, keyboardEvent):
        vec = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Player").Transform.Translation.y + 8), 0)
        vec2 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Player").Transform.Translation.y + 7), 0)
        vec3 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Player").Transform.Translation.y + 6.5), 0)
        vec4 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Player").Transform.Translation.y + 5.5), 0)
        #If tab is pressed then toggle pausing the game
        if(keyboardEvent.Key == Keys.P and self.Pause == False):
            self.Space.CreateAtPosition("Pause", vec)
            self.Space.CreateAtPosition("QuitLevel", vec3)
            self.Space.CreateAtPosition("PauseBG", vec2)
            self.Space.CreateAtPosition("QuitGame", vec4)
            self.Pause = True
            self.Space.TimeSpace.TogglePause()
        elif(keyboardEvent.Key == Keys.P and self.Pause == True):
            self.Space.FindObjectByName("Pause").Destroy()
            self.Space.FindObjectByName("QuitLevel").Destroy()
            self.Space.FindObjectByName("PauseBG").Destroy()
            self.Space.FindObjectByName("QuitGame").Destroy()

            self.Pause = False
            self.Space.TimeSpace.TogglePause()
        if(keyboardEvent.Key == Keys.Back):
            self.Pause = False
            self.Space.TimeSpace.TogglePause()
            if(Zero.Game.FindSpaceByName("HUDSpace")):
                Zero.Game.FindSpaceByName("HUDSpace").Destroy()
            self.Space.LoadLevel("MainMenu")
            

            
         
            
            
            
            
    #load pause level with new cursor 
Zero.RegisterComponent("GlobalTime", GlobalTime)