import Zero
import Events
import Property
import VectorMath
import random
import math
import Color

Vec3 = VectorMath.Vec3

class BatEnemy:
    
    temp = 0
    ranNum = 0
    ranDenom = 0
    maxMoveDistance = Property.Float(5.0)
    ChaseTriggerDistance = Property.Float(7.0)
    ChaseSpeed = Property.Float(5.0)
    Health = Property.Int(3)
    PaceLength = Property.Float(50.0)
    PaceSpeed = Property.Float(1.0)
    Stun = Property.Int(5)
    StunState = False
    
    HomeQ = True
        
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        self.StartPosition = self.Owner.Transform.Translation
        self.DistanceFromTarget = 0.0
        self.StunTimer = 0
        self.ChaseDirection = Vec3(0,0,0)
        self.OriginalColor = self.Owner.Sprite.Color
        self.ChaseColor = Color.Green
        self.player = self.Space.FindObjectByName("Player")
        
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        
    def OnLogicUpdate(self, UpdateEvent):
        
        targetIsWithinRange = False
        
        if(self.StunTimer > 0):
            self.StunTimer -= UpdateEvent.Dt
        if(self.StunTimer <= 0):
            self.StunState = False
            self.StunTimer = 0
                    
        if(self.StunState):
            #print("Stun")
            self.Owner.Sprite.Color = Color.Yellow
            #For Grapple
            self.Owner.Name = ("Floor")

        else:
            #print("UnStun")
            #Ungrapple
            #Logic for updating distance from target and chase direction 
            self.CalculateChaseDirectionAndDistance()
            #Determines whether or not to chase of pace 
            targetIsWithinRange = (self.DistanceFromTarget <= self.ChaseTriggerDistance)
            
            #If valid object and target is within range 
            if(targetIsWithinRange):
                self.HomeQ = False
                self.ChaseTarget(UpdateEvent)
            else:
                if(self.HomeQ == False):
                    self.GoHome()
                else:
                    self.Owner.Sprite.Color = self.OriginalColor
                    self.IdleMovePattern(UpdateEvent)
            self.Owner.Name = ("Bat")
            
        
    def GoHome(self):
        
        direction = (self.StartPosition - self.Owner.Transform.Translation)
        
        if(direction.length() <= 0.5):
            self.HomeQ = True
        
        direction.normalize()
        self.Owner.Transform.Translation += direction
        
    def IdleMovePattern(self, UpdateEvent):
        self.Owner.Transform.Translation += Vec3(math.cos(self.temp * 0.75), math.sin(self.temp), 0) * UpdateEvent.Dt * self.PaceLength
        
        
        self.temp += 0.15 * self.PaceSpeed

    def GenerateRandomValues(self):
        self.ranNum = random.randint(1, 50)
        self.ranDenom = random.randint(2, 5)
        
        
    def ChaseTarget(self, UpdateEvent):
        #Set Chase Color 
        self.Owner.Sprite.Color = self.ChaseColor
        #Apply movement 
        self.Owner.Transform.Translation += self.ChaseDirection * UpdateEvent.Dt * self.ChaseSpeed
        
        
    def CalculateChaseDirectionAndDistance(self):
        #Get direction towards target 
        self.ChaseDirection = self.player.Transform.Translation - self.Owner.Transform.Translation
        #Get distance from target 
        self.DistanceFromTarget = self.ChaseDirection.length()
        #Only want unit length direction 
        self.ChaseDirection.normalize()
        
    def OnCollisionStart(self, CollisionEvent):
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            self.StunState = True
            self.StunTimer = 5
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.Owner.Sprite.Color = Color.Blue
            #self.Owner.ForceEffect.Direction = (self.Space.FindObjectByName("Player").Transform.Translation - self.Owner.Transform.Translation)
            
    def OnCollisionEnd(self, CollisionEvent):
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.Owner.Sprite.Color
        

Zero.RegisterComponent("BatEnemy", BatEnemy)