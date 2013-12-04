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
        Zero.Connect(Zero.Game, Events.GameRequestQuit, self.OnGameRequestQuit)
        
    def OnKeyDown(self, keyboardEvent):
        self.Target = self.Space.FindObjectByName("Target")
        vec = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Camera").Transform.Translation.y + 2.7), 10)
        vec2 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Camera").Transform.Translation.y + -.3), 9)
        vec3 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Camera").Transform.Translation.y + .1), 10)
        vec4 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Camera").Transform.Translation.y + -3.5), 10)
        vec5 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Camera").Transform.Translation.y + 1.3), 10)
        vec6 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Camera").Transform.Translation.y + -1.1), 10)
        vec7 = Vec3(self.Space.FindObjectByName("Camera").Transform.Translation.x, (self.Space.FindObjectByName("Camera").Transform.Translation.y + -2.3), 10)
        if(self.Pause == True):
            if(Zero.Keyboard.KeyIsPressed(Zero.Keys.M)):
                self.Space.SoundSpace.Pause = not self.Space.SoundSpace.Pause
        #If tab is pressed then toggle pausing the game
        if(keyboardEvent.Key == Keys.P and self.Pause == False):
            self.Space.CreateAtPosition("Pause", vec)
            self.Space.CreateAtPosition("QuitLevel", vec7)
            self.Space.CreateAtPosition("PauseBG", vec2)
            self.Space.CreateAtPosition("QuitGame", vec4)
            self.Space.CreateAtPosition("PauseP", vec5)
            self.Space.CreateAtPosition("PauseM", vec3)
            self.Space.CreateAtPosition("PauseMM", vec6)
            self.Pause = True
            self.Space.TimeSpace.TogglePause()

            #self.Target.Sprite.Visible = False
            #Zero.Cursor = 0
            
        elif(keyboardEvent.Key == Keys.P and self.Pause == True):
            self.Space.FindObjectByName("Pause").Destroy()
            self.Space.FindObjectByName("QuitLevel").Destroy()
            self.Space.FindObjectByName("PauseBG").Destroy()
            self.Space.FindObjectByName("QuitGame").Destroy()
            self.Space.FindObjectByName("PauseP").Destroy()
            self.Space.FindObjectByName("PauseM").Destroy()
            self.Space.FindObjectByName("PauseMM").Destroy()
            #self.Target.Sprite.Visible = True
            #Zero.Cursor = -1
            self.Pause = False
            self.Space.TimeSpace.TogglePause()
            
        if(self.Pause):
            if(keyboardEvent.Key == Keys.Back):
                self.Pause = False
                self.Space.TimeSpace.TogglePause()
                if(Zero.Game.FindSpaceByName("HUDSpace")):
                    Zero.Game.FindSpaceByName("HUDSpace").Destroy()
                self.Space.LoadLevel("MainMenu")
            
        if(keyboardEvent.Key == Keys.Escape and self.Pause == False):
            self.Space.CreateAtPosition("PauseBG", vec2)
            self.Space.CreateAtPosition("EscQuit", vec)
            self.Space.CreateAtPosition("EscQuitY", vec3)
            self.Space.CreateAtPosition("EscQuitN", vec7)
            self.Pause = True
            self.Space.TimeSpace.TogglePause()
            
        elif(keyboardEvent.Key == Keys.N and self.Pause == True):
            self.Space.FindObjectByName("PauseBG").Destroy()
            self.Space.FindObjectByName("EscQuit").Destroy()
            self.Space.FindObjectByName("EscQuitY").Destroy()
            self.Space.FindObjectByName("EscQuitN").Destroy()
            self.Pause = False
            self.Space.TimeSpace.TogglePause()
            
        elif(keyboardEvent.Key == Keys.Y and self.Pause == True):
            Zero.Game.Quit()
            
            
            
    def OnGameRequestQuit(self, gameEvent):
        #If you handle this event the game will not exit
        gameEvent.Handled = True
            
            
            
            
    #load pause level with new cursor 
Zero.RegisterComponent("GlobalTime", GlobalTime)