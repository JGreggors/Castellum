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
        vec = Vec3(self.Space.FindObjectByName("Player").Transform.Translation.x, (self.Space.FindObjectByName("Player").Transform.Translation.y + 6), 0)
        #If tab is pressed then toggle pausing the game
        if(keyboardEvent.Key == Keys.P and self.Pause == False):
            self.Space.CreateAtPosition("Pause", vec)
            self.Pause = True
            self.Space.TimeSpace.TogglePause()
        elif(keyboardEvent.Key == Keys.P and self.Pause == True):
            self.Space.FindObjectByName("Pause").Destroy()
            self.Pause = False
            self.Space.TimeSpace.TogglePause()
            
            
            
            
    #load pause level with new cursor 
Zero.RegisterComponent("GlobalTime", GlobalTime)