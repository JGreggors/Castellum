import Zero
import Events
import Property
import VectorMath
import Property

class Timer:
    par = Property.Float(120.0)
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.hudSpace = Zero.Game.FindSpaceByName("HUDSpace")
        self.totalTime = 0.0
        self.secondsPassed = 0.0
        self.carry = 0
        self.par = 80
        
    def OnLogicUpdate(self, UpdateEvent):
        self.secondsPassed += UpdateEvent.Dt
        self.totalTime += UpdateEvent.Dt
            
        
        if(not self.hudSpace):
            print("you ain't got no hudSpace...or maybe i just couldn't find it :(")
            return
            
        timeObject = self.hudSpace.FindObjectByName("Timer")
            
        carryObject = self.hudSpace.FindObjectByName("Carry")
        
        timeObject.SpriteText.Text = str(round(self.secondsPassed, 1))
        
        if(self.carry == 0):
            carryObject.SpriteText.Text = "0"
        
        if(self.secondsPassed > 60.0):
            self.secondsPassed = 0.0
            self.carry += 1
            if(self.carry == 1):
                carryObject.SpriteText.Text = "I"
            elif(self.carry == 2):
                carryObject.SpriteText.Text = "II"
            elif(self.carry == 3):
                carryObject.SpriteText.Text = "III"
            elif(self.carry == 4):
                carryObject.SpriteText.Text = "VI"
            elif(self.carry == 5):
                carryObject.SpriteText.Text = "V"
                
        if(self.totalTime > self.par):
            self.Space.FindObjectByName("Player").Health.Health = 0
            self.carry = 0
            self.totalTime = 0.0
            self.secondsPassed = 0.0

Zero.RegisterComponent("Timer1", Timer)