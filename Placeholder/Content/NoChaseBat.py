import Zero
import Events
import Property
import VectorMath
import Color

Vec3 = VectorMath.Vec3

class NoChaseBat:
    
    PaceSpeed = Property.Float(5.0)
    MaxMoveDistance = Property.Float(5.0)
    Stun = Property.Int(5)
    MoveDirection = Property.Vector3(Vec3(0,0,0))
    
    stunDelay = Property.Float(1.0)
    
    StunState = False
    
    def Initialize(self, initializer):
        #We need to update the enemy's behavior every logic update 
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #Initialize member variables 
        
        self.StartPosition = self.Owner.Transform.Translation
        self.OriginalColor = self.Owner.Sprite.Color
        self.StunTimer = 0.0
        
        self.nextPing = 0.0
        
        self.five = False
        self.four = False
        self.three = False
        self.two = False
        self.one = False
        
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
            self.Owner.Sprite.Color = self.OriginalColor
            targetIsWithinRange = False
            self.Owner.Name = ("Bat")
            
            
            self.PaceBackAndForth(UpdateEvent)
            
        if(self.StunState == True):
            self.StunLogic()
            #print("Stun")
            self.Owner.Sprite.Color = Color.Green
            #For Grapple
            self.Owner.Name = ("Floor")
        
        if(UpdateEvent.CurrentTime > self.nextPing):
            self.nextPing = UpdateEvent.CurrentTime + self.stunDelay
            if(self.StunState == True):
                self.Space.SoundSpace.PlayCue("stun")
        
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
        
    def StunLogic(self):
        self.five = True
        self.four = True
        self.three = True
        self.two = True
        self.one = True
        if(self.StunTimer > 4.95 and self.StunTimer < 5):
            self.Space.CreateAtPosition("five", (self.Owner.Transform.Translation + Vec3(0, 0.5, 0)))
            self.five = False
        elif(self.StunTimer > 3.95 and self.StunTimer < 4):
            self.Space.CreateAtPosition("four", (self.Owner.Transform.Translation + Vec3(0, 0.5, 0)))
            self.four = False
        elif(self.StunTimer > 2.95 and self.StunTimer < 3):
            self.Space.CreateAtPosition("three", (self.Owner.Transform.Translation + Vec3(0, 0.5, 0)))
            self.three = False
        elif(self.StunTimer > 1.95 and self.StunTimer < 2):
            self.Space.CreateAtPosition("two", (self.Owner.Transform.Translation + Vec3(0, 0.5, 0)))
            self.two = False
        elif(self.StunTimer > 0.95 and self.StunTimer < 1):
            self.Space.CreateAtPosition("one", (self.Owner.Transform.Translation + Vec3(0, 0.5, 0)))
            self.one = False
        
    def OnCollisionStart(self, CollisionEvent):
        
        if(CollisionEvent.OtherObject.Name == "Player"):
            self.Owner.Sprite.Color = Color.Blue
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            self.StunState = True
            self.StunTimer = 5
            


Zero.RegisterComponent("NoChaseBat", NoChaseBat)