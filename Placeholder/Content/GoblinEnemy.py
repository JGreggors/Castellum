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
    Stun = Property.Int(5)
    MaxPaceDistance = Property.Float(5.0)
    #jumpHeight = Property.Int(1)
    
    HomeQ = True
    StunState = False
    
    def Initialize(self, initializer):
        #We need to update the enemy's behavior every logic update 
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #Initialize member variables 
        
        self.PaceDirection = Vec3(1,0,0)
        self.StartPosition = self.Owner.Transform.Translation
        self.DistanceFromHome = 0.0
        self.DistanceFromTarget = 0.0
        self.homeDirection = Vec3(0,0,0)
        self.ChaseDirection = Vec3(0,0,0)
        self.OriginalColor = self.Owner.Sprite.Color
        self.ChaseColor = Color.Blue
        self.StunTimer = 0.0
        self.AfterAttack = False
        #self.StunCounter = 0
        
        #self.OnGround = False
        
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)

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
            reachMaxRange = (self.DistanceFromHome >= self.MaxMoveDistance)
            
            #If valid object and target is within range 

            if(targetIsWithinRange and self.AfterAttack == False):
                if(reachMaxRange):
                    self.AfterAttack = True
                else:
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
            self.AfterAttack = False
            
        
        direction.normalize()
        self.Owner.Transform.Translation += direction * 0.25
        
    def PaceBackAndForth(self, UpdateEvent):
            
        displacement = self.Owner.Transform.Translation - self.StartPosition
        #How far from starting position 
        distanceFromStart = displacement.length()
        
        #We want to change direction after 
        #reaching the max move distance from starting position 
        if(distanceFromStart >= self.MaxPaceDistance):
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
        #if(self.ChaseDirection.y > self.Owner.Transform.Translation.y):
            #self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(0,self.jumpHeight,0))
            
#------------------------------------------------------------------------------------------------------------
    #def CanJump(self):
    #    canJump = self.OnGround
    #    return canJump
        
    #def UpdateGroundState(self):
    #    self.OnGround = False
    #    #Testing if objects are 'ground'
    #    for ContactHolder in self.Owner.Collider.Contacts:
    #        #Ignore ghost objects
    #        if(ContactHolder.IsGhost):
    #            continue
    #        objectHit = ContactHolder.OtherObject
    #        surfaceNormal = -ContactHolder.FirstPoint.WorldNormalTowardsOther
    #        #If the object is considered walkable
    #        if(self.IsGround(surfaceNormal)):
    #            self.OnGround = True
    #            return
                
    #def GetDegreeDifference(self, surfaceNormal):
    #    #Using angles to test if something is 'Ground'
    #    UpDirection = Vec3(0,1,0)
    #    cosTheta = surfaceNormal.dot(UpDirection)
    #    radians = math.acos(cosTheta)
    #    degrees = math.degrees(radians)
    #    return degrees
        
    #def IsGround(self, surfaceNormal):
    #    #defines what is ground
    #    degrees = self.GetDegreeDifference(surfaceNormal)
    #    return degrees < 60.0
        
#---------------------------------------------------------------------------------------------------------------
    def CalculateChaseDirectionAndDistance(self):
        targetObject = self.Space.FindObjectByName("Player") 
        #Get direction towards target 
        self.ChaseDirection = targetObject.Transform.Translation - self.Owner.Transform.Translation
        self.homeDirection = self.StartPosition - self.Owner.Transform.Translation
        #Get distance from target 
        self.DistanceFromTarget = self.ChaseDirection.length()
        self.DistanceFromHome = self.homeDirection.length()
        #Only want unit length direction 
        self.homeDirection.normalize()
        self.ChaseDirection.normalize()
           
        
    def OnCollisionStart(self, CollisionEvent):
        
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            self.StunState = True
            self.StunTimer = 5
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.AfterAttack = True


Zero.RegisterComponent("GoblinEnemy", GoblinEnemy)