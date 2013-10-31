import Zero
import Events
import Property
import VectorMath
import Color

class LeverLogic:
    
    access = False #is the switch switched?
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.Switchgate1 = self.Space.FindObjectByName("SwitchGate1")
        self.Switchgate2 = self.Space.FindObjectByName("SwitchGate2")
        
        self.startGate1 = self.Switchgate1.Transform.Translation
        self.startGate2 = self.Switchgate2.Transform.Translation
        
        self.yAxis = 0.0 #the amount of up or down the gate is
        
    def OnLogicUpdate(self, UpdateEvent):
        # If open gates move
        if(self.access == True):
            self.yAxis += UpdateEvent.Dt
            self.Space.FindObjectByName("Lever").Sprite.Color = Color.Black
            self.Switchgate2.Transform.Translation = self.startGate2 + VectorMath.Vec3(0, -self.yAxis, 0)
            self.Switchgate1.Transform.Translation = self.startGate1 + VectorMath.Vec3(0, self.yAxis, 0)
            #Until max then set doors there
            if(self.yAxis > 3):
                print("blamo")
                self.yAxis += 0
                self.startGate1 = self.Switchgate1.Transform.Translation
                self.startGate2 = self.Switchgate2.Transform.Translation
        #Limit for gate raising
        if(self.yAxis > 3):
            self.access = False
        
        
    def OnCollisionStart(self, CollisionEvent):
        otherObject = CollisionEvent.OtherObject
        #if it gets shot initiate
        if(otherObject.Name == "Projectile"):
            self.access = True
            self.Owner.BoxCollider.SendsEvents = False

                



Zero.RegisterComponent("LeverLogic", LeverLogic)