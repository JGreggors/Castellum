import Zero
import Events
import Property
import VectorMath

class DoorLogic:
    
    access = False
    
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollisionPersisted)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        self.gate1 = self.Space.FindObjectByName("Gate1")
        self.gate2 = self.Space.FindObjectByName("Gate2")
        self.startGate1 = self.gate1.Transform.Translation
        self.startGate2 = self.gate2.Transform.Translation
        self.yAxis = 0.0
        
    def OnLogicUpdate(self, UpdateEvent):
        if(self.access == True):
            self.yAxis += UpdateEvent.Dt
        
    def OnCollisionPersisted(self, CollisionEvent):
        keyAttached = self.Space.FindObjectByName("Player").MasterPlayerContr.keyAttached
        otherObject = CollisionEvent.OtherObject
        key = self.Space.FindObjectByName("Key")
            
        if(otherObject.Name == "Player" and keyAttached == True):
            #print("open")
            self.access = True
            self.gate2.Transform.Translation = self.startGate2 + VectorMath.Vec3(0, -self.yAxis, 0)
            self.gate1.Transform.Translation = self.startGate1 + VectorMath.Vec3(0, self.yAxis, 0)

            if(self.yAxis > 0.5):
                #print("blamo")
                self.yAxis += 0
                self.startGate1 = self.gate1.Transform.Translation
                self.startGate2 = self.gate2.Transform.Translation
                self.Space.FindObjectByName("Player").MasterPlayerContr.keyAttached = False
                self.Space.FindObjectByName("Player").MasterPlayerContr.CanShoot = True
                key.Destroy()
    def OnCollisionStart(self, CollisionEvent):
        keyAttached = self.Space.FindObjectByName("Player").MasterPlayerContr.keyAttached
        if(CollisionEvent.OtherObject.Name == "Player" and keyAttached == True):
            self.Space.SoundSpace.PlayCue("opengate")
      
            

Zero.RegisterComponent("DoorLogic", DoorLogic)