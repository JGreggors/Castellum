import Zero
import Events
import Property
import VectorMath
import Color

Vec3 = VectorMath.Vec3

class GoblinEnemy:
    
    #Pacing Properties 
    PaceSpeed = Property.Float(5.0)
    MaxMoveDistance = Property.Float(5.0)
    #Chasing Properties 
    ChaseTriggerDistance = Property.Float(7.0)
    ChaseSpeed = Property.Float(5.0)
    Health = Property.Int()
    Stun = Property.Int(5)
    
    HomeQ = True
    StunState = False
    
    def Initialize(self, initializer):
        #We need to update the enemy's behavior every logic update 
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #Initialize member variables 
        
        self.PaceDirection = Vec3(1,0,0)
        self.StartPosition = self.Owner.Transform.Translation
        self.DistanceFromTarget = 0.0
        self.ChaseDirection = Vec3(0,0,0)
        self.OriginalColor = self.Owner.Sprite.Color
        self.ChaseColor = Color.Blue
        self.StunTimer = 0.0
        #self.StunCounter = 0
        
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        Zero.Connect(self.Owner, Events.CollisionEnded, self.OnCollisionEnd)
        
    def OnLogicUpdate(self, UpdateEvent):
        #print(self.ChaseDirection)
        #We will re-evaluate this every logic update 
        if(self.StunTimer > 0):
            self.StunTimer -= UpdateEvent.Dt
        if(self.StunTimer <= 0):
            self.StunState = False
            self.StunTimer = 0
            
        if(self.StunState == False):
            
            targetIsWithinRange = False
            self.Owner.Name = ("Goblin")
            
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
                    self.PaceBackAndForth(UpdateEvent)
                    #Logic for pacing back and forth 
            self.PaceBackAndForth(UpdateEvent)
            
        if(self.StunState == True):
            #print("Stun")
            self.Owner.Sprite.Color = Color.Yellow
            #For Grapple
            self.Owner.Name = ("Floor")


        
    def GoHome(self):
        
        direction = (self.StartPosition - self.Owner.Transform.Translation)
        
        if(direction.length() <= 0.5):
            self.HomeQ = True
        
        direction.normalize()
        self.Owner.Transform.Translation += direction * 0.25
        
    def PaceBackAndForth(self, UpdateEvent):
            
        displacement = self.Owner.Transform.Translation - self.StartPosition
        #How far from starting position 
        distanceFromStart = displacement.length()
        
        #We want to change direction after 
        #reaching the max move distance from starting position 
        if(distanceFromStart >= self.MaxMoveDistance):
            self.PaceDirection = -displacement
            
            #Only want unti length direction
            self.PaceDirection.normalize()
            
        
        #Apply movement 
        self.Owner.Transform.Translation += self.PaceDirection * UpdateEvent.Dt * self.PaceSpeed
        
    def ChaseTarget(self, UpdateEvent):
        #Set Chase Color 
        self.Owner.Sprite.Color = self.ChaseColor
        #Apply movement 
        self.Owner.Transform.Translation += self.ChaseDirection * UpdateEvent.Dt * self.ChaseSpeed
        
        
    def CalculateChaseDirectionAndDistance(self):
        targetObject = self.Space.FindObjectByName("Player") 
        #Get direction towards target 
        self.ChaseDirection = targetObject.Transform.Translation - self.Owner.Transform.Translation
        self.ChaseDirection *= Vec3(1,0,1)
        #Get distance from target 
        self.DistanceFromTarget = self.ChaseDirection.length()
        #Only want unit length direction 
        self.ChaseDirection.normalize()
           
        
    def OnCollisionStart(self, CollisionEvent):
        
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.Owner.Sprite.Color = Color.Blue
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            self.StunState = True
            self.StunTimer = 5
            
    def OnCollisionEnd(self, CollisionEvent):
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.Owner.Sprite.Color
            

Zero.RegisterComponent("GoblinEnemy", GoblinEnemy)