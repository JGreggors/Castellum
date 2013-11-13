import Zero
import Events
import Property
import VectorMath
import Property

class Timer:
    #level par
    par = Property.Float(45.0)
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.totalTime = 0.0
        
        #for the clock
        self.secondsPassed = self.par - (60.0 * (round(self.par / 60) - 1))
        self.carry = (round(self.par / 60) - 1)
        
        self.starttime = self.secondsPassed
        self.startcarry = self.carry
        
        
    def OnLogicUpdate(self, UpdateEvent):
        #start the timer
        #print(self.carry)
        self.secondsPassed -= UpdateEvent.Dt
        self.totalTime += UpdateEvent.Dt
        #print(round(self.par / 60 ) - 1)

            
        #find the hud
       #----------------------------------------------------------------------------
        hudSpace = Zero.Game.FindSpaceByName("HUDSpace")
        if(not hudSpace):
            pass
            
        timeObject = hudSpace.FindObjectByName("Timer")
            
        carryObject = hudSpace.FindObjectByName("Carry")
        
        if(timeObject):
            timeObject.SpriteText.Text = str(round(self.secondsPassed, 1))
       #----------------------------------------------------------------------------
        
        #When there is no carry
        if(self.carry == 0):
            carryObject.SpriteText.Text = "0"
        if(self.carry == 1):
            carryObject.SpriteText.Text = "I"
        if(self.carry == 2):
            carryObject.SpriteText.Text = "II"
        if(self.carry == 3):
            carryObject.SpriteText.Text = "III"
        if(self.carry == 4):
            carryObject.SpriteText.Text = "VI"
        if(self.carry == 5):
            carryObject.SpriteText.Text = "V"
        #after 60 seconds add a carry and reset to zero

        if(self.secondsPassed < 0.0):
            self.secondsPassed = 60.0
            self.carry = round(self.carry - 1)

        
        #If you time is greater than the par of the level YOU DIE!
        if(self.totalTime > self.par):
            self.Space.FindObjectByName("Player").Health.Health = 0
            self.carry = self.startcarry
            self.totalTime = 0.0
            self.secondsPassed = self.starttime

Zero.RegisterComponent("Timer", Timer)