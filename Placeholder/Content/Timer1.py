import Zero
import Events
import Property
import VectorMath
import Property

class Timer1:
    par = Property.Float(45.0)
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.totalDeath = 0
        self.gold = 0
        self.totalTime = 0.0
        self.secondsPassed = 0.0
        self.carry = 0
        
    def OnLogicUpdate(self, UpdateEvent):
        self.secondsPassed += UpdateEvent.Dt
        self.totalTime += UpdateEvent.Dt
        
        
        #self.GoldPickup = self.Space.FindObjectByName("Player").PickupGold.PlusOne
            
        hudSpace = Zero.Game.FindSpaceByName("HUDSpace")
        if(not hudSpace):
            pass

            
        timeObject = hudSpace.FindObjectByName("Timer")
            
        carryObject = hudSpace.FindObjectByName("Carry")
        
        timeObject.SpriteText.Text = str(round(self.secondsPassed, 1))
        
        if(self.carry == 0):
            carryObject.SpriteText.Text = "0"
        
        if(self.secondsPassed > 60.0):
            self.secondsPassed = 0.0
            self.carry += 1
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
                
        if(self.totalTime > self.par):
            self.Space.FindObjectByName("Player").Health.Health = 0
            self.carry = 0
            self.totalTime = 0.0
            self.secondsPassed = 0.0
            
       
            
        #print(self.gold)
        print(self.totalDeath)

Zero.RegisterComponent("Timer", Timer1)