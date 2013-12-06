########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class StartScreenLogic:
#for splash screens and title screen
#also used during presentations

    def Initialize(self, initializer):
        
        #Creating an update  event
        Zero.Connect(self.Space, Events.LogicUpdate, self.onLogicUpdate)
        
        #variables for slides and switching between them
        self.slideNum = 1
        self.swap = False
        self.lastSlide = 2
        self.maxcount = 4
        self.count = 4
        
        #making the cursor invisible
        Zero.Mouse.Cursor = -1
        
    def onLogicUpdate(self, UpdateEvent):
        
        #setting slide to slide object in level
        self.slide = self.Space.FindObjectByName("Slide" + str(self.slideNum))
        
        #timer for how long slide should be displayed
        if(self.count <= 4):
            self.count -= UpdateEvent.Dt
        if(self.count < 0):
            self.count = self.maxcount
            self.swap = True
            self.slideNum += 1
            self.prevSlide = self.Space.FindObjectByName("Slide" + str(self.slideNum-1))

        #swap slides when timer ends
        if(self.swap):
            self.swapSlides()
        
        #fades in first slide
        if(self.slideNum == 1 and self.slide.Sprite.Color.w < 1):
            self.fadeIn()
        
    def swapSlides(self):
        #fade out second slide
        if(self.slideNum == self.lastSlide + 1):
            self.fadeOut()
            #load main menu when faded out
            if(self.prevSlide.Sprite.Color.w == 0):
                self.Space.LoadLevel("MainMenu")
        #fade out first slide
        else:
            if(self.prevSlide.Sprite.Color.w > 0):
                self.fadeOut()
            #fade in new slide
            elif(self.slide.Sprite.Color.w < 1):
                self.fadeIn()
        
#--------------------------------------------------------------------------
#Functions for fading in and fading out slides

    def fadeIn(self):
        if(self.slide.Sprite.Color.w + 0.01 >= 1):
            self.slide.Sprite.Color = VectorMath.Vec4(1,1,1,1)
        else:
            self.slide.Sprite.Color += VectorMath.Vec4(0,0,0,0.005)
            
            
    def fadeOut(self):
        if(self.prevSlide.Sprite.Color.w - 0.01 <= 0):
            self.prevSlide.Sprite.Color = VectorMath.Vec4(1,1,1,0)
        else:
            self.prevSlide.Sprite.Color -= VectorMath.Vec4(0,0,0,0.01)
#--------------------------------------------------------------------------

Zero.RegisterComponent("StartScreenLogic", StartScreenLogic)