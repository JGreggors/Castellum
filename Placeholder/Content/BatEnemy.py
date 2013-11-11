import Zero
import Events
import Property
import VectorMath
import random
import math
import Color

Vec3 = VectorMath.Vec3

class BatEnemy:
    
    temp = 0 #stores trajectory
    ranNum = 0 #numerator for fraction
    ranDenom = 0 # denominator for fraction
    maxMoveDistance = Property.Float(5.0)
    ChaseTriggerDistance = Property.Float(7.0)
    ChaseSpeed = Property.Float(5.0)
    PaceLength = Property.Float(50.0)
    PaceSpeed = Property.Float(1.0)
    Stun = Property.Int(5)
    ReturnSpeed = Property.Float(10.0)
    
    HomeQ = True #is he home?
    StunState = False
    UpQ = False #Is the bat up?
    def Initialize(self, initializer):
        #connects to BatTime
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #set variables
       #-----------------------------------------------------------------------------
        self.StartPosition = self.Owner.Transform.Translation
        self.DistanceFromTarget = 0.0
        self.StunTimer = 0
        self.ChaseDirection = Vec3(0,0,0)
        self.OriginalColor = self.Owner.Sprite.Color
        self.ChaseColor = Color.Green
        self.player = self.Space.FindObjectByName("Player")
        self.AfterAttack = False
        self.LeaveTime = 0.0
       #-----------------------------------------------------------------------------
        
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
    def OnLogicUpdate(self, UpdateEvent):
        #print(self.AfterAttack)
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
            if(targetIsWithinRange and self.AfterAttack == False):
                self.HomeQ = False
                self.ChaseTarget(UpdateEvent)
            else:
                if(self.HomeQ == False):
                    if(self.UpQ == False):
                        self.GoUp(UpdateEvent)
                    else:
                        self.GoHome(UpdateEvent)
                        
                else:
                    self.Owner.Sprite.Color = self.OriginalColor
                    self.IdleMovePattern(UpdateEvent)
            self.Owner.Name = ("Bat")
            
    def GoHome(self, UpdateEvent):
        
        direction = (self.StartPosition - self.Owner.Transform.Translation)
        
        if(direction.length() <= 0.5):
            self.Owner.Transform.Translation = self.StartPosition
            self.HomeQ = True
            self.AfterAttack = False
            self.UpQ = False
        
        direction.normalize()
        self.Owner.Transform.Translation += direction * UpdateEvent.Dt * self.ReturnSpeed
        
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
        
    def GoUp(self, UpdateEvent):
        
        #Set the direction for movment
        UpPoint = Vec3((self.Owner.Transform.Translation.x - self.StartPosition.x) / 2, self.StartPosition.y + 10, 0)
        UpDirection = UpPoint - self.Owner.Transform.Translation
        #Check to see if the distance is greater than a value (Close to the end point)
        if(UpDirection.length() <= 1):
            self.Owner.Transform.Translation = UpPoint
            self.UpQ = True
        else:
            #If yes (still has time to go) normalize the direction vector, and add it to the bat vector
            UpDirection.normalize()
            self.Owner.Transform.Translation += UpDirection * UpdateEvent.Dt * self.ReturnSpeed
        
        #If not set UPQ to true, this will make it go home.  BE SURE TO RESET THESE BOOL VALUES IN EACH STEP OF THE WAY 1.CHASETARGET 2.GOUP 3.GOHOME
        
        
    def CalculateChaseDirectionAndDistance(self):
        #Get direction towards target 
        self.ChaseDirection = self.player.Transform.Translation - self.Owner.Transform.Translation
        #Get distance from target 
        self.DistanceFromTarget = self.ChaseDirection.length()
        #Only want unit length direction 
        self.ChaseDirection.normalize()
        
    def OnCollisionStart(self, CollisionEvent):
        #print("Sup Bitch")
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.AfterAttack = True
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            self.StunState = True
            self.StunTimer = 5


Zero.RegisterComponent("BatEnemy", BatEnemy)