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

class GoblinTime:
    IO = True
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.StunCounter = 0
        
    def OnLogicUpdate(self, UpdateEvent):
        #print(self.StunCounter)
        GoblinTime = Zero.ScriptEvent()
        if(self.IO == True):
            GoblinTime.Dt = UpdateEvent.Dt
            self.Space.DispatchEvent("gPause", GoblinTime)
            
        elif(self.IO == False):
            self.StunCounter += UpdateEvent.Dt
            if(self.StunCounter > 5):
                self.StunCounter = 0
                self.IO = True

Zero.RegisterComponent("GoblinTime", GoblinTime)