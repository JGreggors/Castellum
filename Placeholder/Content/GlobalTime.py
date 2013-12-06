########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Keys 
import Action
import math

#Making a shortcut for VectorMath.Vec3
Vec3 = VectorMath.Vec3

class GlobalTime:
#Logic for Pausing Game as well as Pause and Escape Menus
    
    def Initialize(self, init):
        #Setting up a Keyboard Event
        Zero.Connect(Zero.Keyboard, Events.KeyDown, self.OnKeyDown)
       
        #Setting Pause states  to False
        self.Pause = False  #For when player pauses game
        self.Escape = False #For when player trys to quit game
        
        #Setting up a way to intersect the quit even if player presses Esc
        Zero.Connect(Zero.Game, Events.GameRequestQuit, self.OnGameRequestQuit)
        
    def OnKeyDown(self, keyboardEvent):
        
        #setting variable for cursor reticle
        self.Target = self.Space.FindObjectByName("Target")
        self.Camera = self.Space.FindObjectByName("Camera")
        
        #setting up variables for different positions based off of camera position
        vec = Vec3(self.Camera.Transform.Translation.x, (self.Camera.Transform.Translation.y + 2.7), 10)
        vec2 = Vec3(self.Camera.Transform.Translation.x, (self.Camera.Transform.Translation.y + -.3), 9)
        vec3 = Vec3(self.Camera.Transform.Translation.x, (self.Camera.Transform.Translation.y + .1), 10)
        vec4 = Vec3(self.Camera.Transform.Translation.x, (self.Camera.Transform.Translation.y + -3.5), 10)
        vec5 = Vec3(self.Camera.Transform.Translation.x, (self.Camera.Transform.Translation.y + 1.3), 10)
        vec6 = Vec3(self.Camera.Transform.Translation.x, (self.Camera.Transform.Translation.y + -1.1), 10)
        vec7 = Vec3(self.Camera.Transform.Translation.x, (self.Camera.Transform.Translation.y + -2.3), 10)

        #if the player currently doesn't have Escape menu up
        if(self.Escape == False):
            
            # if P is pressed  and the game isn't paused already then toggle pausing the game
            if(keyboardEvent.Key == Keys.P and self.Pause == False):
                
                #Create Pause menu items
                self.Space.CreateAtPosition("Pause", vec)
                self.Space.CreateAtPosition("QuitLevel", vec7)
                self.Space.CreateAtPosition("PauseBG", vec2)
                self.Space.CreateAtPosition("QuitGame", vec4)
                self.Space.CreateAtPosition("PauseP", vec5)
                self.Space.CreateAtPosition("PauseM", vec3)
                self.Space.CreateAtPosition("PauseMM", vec6)
                
                #Set that Pause is true
                self.Pause = True
                #Toggle Pause in TimeSpace
                self.Space.TimeSpace.TogglePause()
            
            #if P is pressed again while the game is paused unpause the game
            elif(keyboardEvent.Key == Keys.P and self.Pause == True):
                
                #Destroy Pause menu items
                self.Space.FindObjectByName("Pause").Destroy()
                self.Space.FindObjectByName("QuitLevel").Destroy()
                self.Space.FindObjectByName("PauseBG").Destroy()
                self.Space.FindObjectByName("QuitGame").Destroy()
                self.Space.FindObjectByName("PauseP").Destroy()
                self.Space.FindObjectByName("PauseM").Destroy()
                self.Space.FindObjectByName("PauseMM").Destroy()

                #Set that the game is not paused
                self.Pause = False
                #Toggle Pause in Timespace
                self.Space.TimeSpace.TogglePause()
            
        #if the game is currently paused
        if(self.Pause):
            
            #if Backspace is pressed unpause game and load MainMenu
            if(keyboardEvent.Key == Keys.Back):
                self.Pause = False
                self.Space.TimeSpace.TogglePause()
                
                #also destroy HUDSpace
                if(Zero.Game.FindSpaceByName("HUDSpace")):
                    Zero.Game.FindSpaceByName("HUDSpace").Destroy()
                
                self.Space.LoadLevel("MainMenu")
                
            #if Escape is pressed Quit the game
            if(keyboardEvent.Key == Keys.Escape):
                self.Escape = True
                Zero.Game.Quit()
                
            #if M is pressed pause sounds
            if(Zero.Keyboard.KeyIsPressed(Zero.Keys.M)):
                self.Space.SoundSpace.Pause = not self.Space.SoundSpace.Pause
        
        #If pause menu is not currently up
        if(self.Pause == False):
            #if player presses Esccape
            if(keyboardEvent.Key == Keys.Escape and self.Escape == False):
                
                #Create Escape menu items
                self.Space.CreateAtPosition("PauseBG", vec2)
                self.Space.CreateAtPosition("EscQuit", vec)
                self.Space.CreateAtPosition("EscQuitY", vec5)
                self.Space.CreateAtPosition("EscQuitN", vec3)
                self.Space.CreateAtPosition("QuitLevel", vec7)
                
                #set that the escape state is on
                self.Escape = True
                #pause the TimeSpace
                self.Space.TimeSpace.TogglePause()
            
            #If player presses N (no) while in escape state
            elif(keyboardEvent.Key == Keys.N and self.Escape == True):
                
                #destroy Escape menu items
                self.Space.FindObjectByName("PauseBG").Destroy()
                self.Space.FindObjectByName("EscQuit").Destroy()
                self.Space.FindObjectByName("EscQuitY").Destroy()
                self.Space.FindObjectByName("EscQuitN").Destroy()
                self.Space.FindObjectByName("QuitLevel").Destroy()
                
                #set that Escape state is off
                self.Escape = False
                #unpausethe TimeSpace
                self.Space.TimeSpace.TogglePause()
            
            #If player presses Y (Yes) while in escape state quit the game
            elif(keyboardEvent.Key == Keys.Y and self.Escape == True):
                Zero.Game.Quit()
            
        #if the game is currently in Escape state
        if(self.Escape):
            
            #if Backspace if pressed set Escape state to off and load MainMenu
            if(keyboardEvent.Key == Keys.Back):
                self.Escape = False
                self.Space.TimeSpace.TogglePause()
                
                #Also destroy HUDSpace if there is one
                if(Zero.Game.FindSpaceByName("HUDSpace")):
                    Zero.Game.FindSpaceByName("HUDSpace").Destroy()
                
                self.Space.LoadLevel("MainMenu")
            
    def OnGameRequestQuit(self, gameEvent):
        #This means the game will not quit when escape is pressed
        gameEvent.Handled = True
            

Zero.RegisterComponent("GlobalTime", GlobalTime)