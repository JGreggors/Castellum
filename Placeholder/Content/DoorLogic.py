########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class DoorLogic:
#Logic to move gates/doors that grant acces with keys
    
    #start acces as false
    access = False
    
    def Initialize(self, initializer):
        
        #Setting up collision event
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnCollisionPersisted)
        #creating update event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        #Creating variables for gate objects
        self.gate1 = self.Space.FindObjectByName("Gate1")
        self.gate2 = self.Space.FindObjectByName("Gate2")
        
        #storing original positions of gates
        self.startGate1 = self.gate1.Transform.Translation
        self.startGate2 = self.gate2.Transform.Translation
        
        #variable for y coordinate
        self.yAxis = 0.0
        
    def OnLogicUpdate(self, UpdateEvent):
        
        #if the gates are opening
        if(self.access == True):
            #increase the y coordinate
            self.yAxis += UpdateEvent.Dt
        
    def OnCollisionPersisted(self, CollisionEvent):
        
        #checking for whether or not player has key
        keyAttached = self.Space.FindObjectByName("Player").MasterPlayerContr.keyAttached
        #variable for collision object
        otherObject = CollisionEvent.OtherObject
        #variable for key object
        key = self.Space.FindObjectByName("Key")
            
        #if the key collides with gate(actually region (GateAOE))
        #gate and gateAOE are parented in an achetype
        if(otherObject.Name == "Player" and keyAttached == True):
            
            #open gates
            self.access = True
            #move one gate up and one gate down
            self.gate2.Transform.Translation = self.startGate2 + VectorMath.Vec3(0, -self.yAxis, 0)
            self.gate1.Transform.Translation = self.startGate1 + VectorMath.Vec3(0, self.yAxis, 0)

            #once the y coordinate reaches max value desired stop the gate
            if(self.yAxis > 0.8):
                
                #reset y variable
                self.yAxis += 0
                #set these new positions at translations of gate
                self.startGate1 = self.gate1.Transform.Translation
                self.startGate2 = self.gate2.Transform.Translation
                #detach key from player and destroy it
                self.Space.FindObjectByName("Player").MasterPlayerContr.keyAttached = False
                key.Destroy()
                
    def OnCollisionStart(self, CollisionEvent):
        
        #checking if key is attached
        keyAttached = self.Space.FindObjectByName("Player").MasterPlayerContr.keyAttached
        #play sound effect when gates open
        if(CollisionEvent.OtherObject.Name == "Player" and keyAttached == True):
            self.Space.SoundSpace.PlayCue("opengate")
            
Zero.RegisterComponent("DoorLogic", DoorLogic)