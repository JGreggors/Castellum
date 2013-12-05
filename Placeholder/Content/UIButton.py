########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

#Creating a shortcut for VectorMath.Vec4
Vec4 = VectorMath.Vec4

class UIButton:
#This is the logic for buttons to work to switch levels
    
    #setting defaults for changing color can change in properties
    DefaultColor = Property.Vector4(default = Vec4(0,212,31,1))
    HoverColor = Property.Vector4(default = Vec4(1,1,0,0.25))
    DownColor = Property.Vector4(default = Vec4(1,1,1,0.5))
    
    #Variable for level index in the level table to switch to
    LevelNumber = Property.Uint(0)
    
    def Initialize(self, initializer):
        #to make color change when mouse hovers
        #and make level change when clicks
        Zero.Connect(self.Owner, Events.MouseEnter, self.OnMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.OnMouseExit)
        Zero.Connect(self.Owner, Events.MouseUp, self.OnMouseUp)
        Zero.Connect(self.Owner, Events.MouseDown, self.OnMouseDown)
        
        #intersepting event that makes game quit when escape is hit
        Zero.Connect(Zero.Game, Events.GameRequestQuit, self.OnGameRequestQuit)
        
        #set the sprite color to it's default
        self.DefaultState()
#----------------------------------------------------------------------
#Color Stuff
    def DefaultState(self):
        self.Owner.SpriteText.Color = self.DefaultColor
        
    def HoverState(self):
        self.Owner.SpriteText.Color = self.HoverColor
        
    def DownState(self):
        self.Owner.SpriteText.Color = self.DownColor
        
    def OnMouseEnter(self, ViewportMouseEvent):
        self.HoverState()
        
    def OnMouseExit(self, ViewportMouseEvent):
        self.DefaultState()
#---------------------------------------------------------------------

#---------------------------------------------------------------------
#For Changing Levels & additional color changes
    def OnMouseUp(self, ViewportMouseEvent):
        #changing color
        self.HoverState()
        
        #Basically if object is called " " go to " " level
        #can change as needed 
        
#---------------------------------------------------------------------
#Main Menu:
    
        #Start
        if(self.Owner.Name == "Start"):
            Zero.Game.LevelManager.LoadSpecificLevel(self.LevelNumber)
            self.Space.SoundSpace.PlayCue("menu")
            
        #Level Select
        elif(self.Owner.Name == "LevelSelect"):
            Zero.Game.LevelManager.LoadSpecificLevel(self.LevelNumber)
            self.Space.SoundSpace.PlayCue("menu")

        #Credits
        elif(self.Owner.Name == "Credits"):
            Zero.Game.LevelManager.LoadSpecificLevel(self.LevelNumber)
            self.Space.SoundSpace.PlayCue("menu")
            
        #High Score Page
        elif(self.Owner.Name == "HighScore"):
            Zero.Game.LevelManager.LoadSpecificLevel(self.LevelNumber)
            self.Space.SoundSpace.PlayCue("menu")
        
        #Quit Button
        elif(self.Owner.Name == "Quit"):
            Zero.Game.Quit()
#---------------------------------------------------------------------
#Back to main menu
            
        elif(self.Owner.Name == "Back"):
            Zero.Game.LevelManager.LoadSpecificLevel(self.LevelNumber)
            self.Space.SoundSpace.PlayCue("menuNo")
            
#---------------------------------------------------------------------
#Level Select Page

        elif(self.Owner.Name == "Level"):
            Zero.Game.LevelManager.LoadSpecificLevel(self.LevelNumber)
            self.Space.SoundSpace.PlayCue("menu")
            
#---------------------------------------------------------------------
#Win screen buttons
            
        elif(self.Owner.Name == "UI"):
            self.Owner.WinScreenLogic.Check()
            
#---------------------------------------------------------------------
       
    def OnMouseDown(self, ViewportMouseEvent):
        #Changing colors
        self.DownState()


    def OnGameRequestQuit(self, gameEvent):
        #this prevents the game from quiting when escape is pressed
        gameEvent.Handled = True
            
            

Zero.RegisterComponent("UIButton", UIButton)