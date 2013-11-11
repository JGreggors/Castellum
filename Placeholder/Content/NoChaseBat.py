import Zero
import Events
import Property
import VectorMath
import Color

Vec3 = VectorMath.Vec3

class NoChaseBat:
    
    #Pacing Properties 
    PaceSpeed = Property.Float(5.0)
    MaxMoveDistance = Property.Float(5.0)
    Stun = Property.Int(5)
    MoveDirection = Property.Vector3(Vec3(0,0,0))
    
    StunState = False
    
    def Initialize(self, initializer):
        #We need to update the enemy's behavior every logic update 
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #Initialize member variables 
        
        self.StartPosition = self.Owner.Transform.Translation
        self.OriginalColor = self.Owner.Sprite.Color
        self.StunTimer = 0.0
        
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
            self.Owner.Name = ("Bat")
            
            
            self.PaceBackAndForth(UpdateEvent)
            
        if(self.StunState == True):
            #print("Stun")
            self.Owner.Sprite.Color = Color.Yellow
            #For Grapple
            self.Owner.Name = ("Floor")
        
    def PaceBackAndForth(self, UpdateEvent):
            
        displacement = self.Owner.Transform.Translation - self.StartPosition
        #How far from starting position 
        distanceFromStart = displacement.length()
        
        #We want to change direction after 
        #reaching the max move distance from starting position 
        if(distanceFromStart >= self.MaxMoveDistance):
            self.MoveDirection = -displacement
            
            #Only want unti length direction
            self.MoveDirection.normalize()
            
        
        #Apply movement 
        self.Owner.Transform.Translation += self.MoveDirection * UpdateEvent.Dt * self.PaceSpeed
        
    def OnCollisionStart(self, CollisionEvent):
        
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.Owner.Sprite.Color = Color.Blue
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            self.StunState = True
            self.StunTimer = 5
            


Zero.RegisterComponent("NoChaseBat", NoChaseBat)