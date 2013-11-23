import Zero
import Events
import Property
import VectorMath

class StartScreenLogic:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.onLogicUpdate)
        self.slideNum = 1
        self.swap = False
        self.lastSlide = 2
        self.maxcount = 4
        self.count = 4
        
    def onLogicUpdate(self, UpdateEvent):
        self.slide = self.Space.FindObjectByName("Slide" + str(self.slideNum))
        
        if(self.count <= 4):
            self.count -= UpdateEvent.Dt
        if(self.count < 0):
            self.count = self.maxcount
            self.swap = True
            self.slideNum += 1
            self.prevSlide = self.Space.FindObjectByName("Slide" + str(self.slideNum-1))
        #if(Zero.Keyboard.KeyIsPressed(Zero.Keys.Back)):
        #    if(self.slideNum != 1):
        #        self.prevSlide = self.slide
        #        self.slideNum -= 1
        #        self.swap = True
        
        if(self.swap):
            self.swapSlides()
        
        if(self.slideNum == 1 and self.slide.Sprite.Color.w < 1):
            self.fadeIn()
        
    def swapSlides(self):
        if(self.slideNum == self.lastSlide + 1):
            self.fadeOut()
            if(self.prevSlide.Sprite.Color.w == 0):
                self.Space.LoadLevel("MainMenu")
        else:
            if(self.prevSlide.Sprite.Color.w > 0):
                self.fadeOut()
            elif(self.slide.Sprite.Color.w < 1):
                self.fadeIn()
        
        
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

Zero.RegisterComponent("StartScreenLogic", StartScreenLogic)