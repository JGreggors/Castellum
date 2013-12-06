########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Color

#shortcut for VectorMath.Vec3
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
    stunDelay = Property.Float(1.0)
    
    #Startiing position
    HomeQ = True
    #Whether enemy is stunned
    StunState = False
    
    def Initialize(self, initializer):
        
        #creating update event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        #Initialize member variables
        #-----------------------------------------------------------------------------
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
        self.alerted = False
        self.nextPing = 0.0
        
        #Numbers for displaying in game time enemy is stunned
        self.five = False
        self.four = False
        self.three = False
        self.two = False
        self.one = False
        #-----------------------------------------------------------------------------
        
        #creaeting a collision event
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)

    def OnLogicUpdate(self, UpdateEvent):
        
        #Countdown for how long enemy should be stunned
        if(self.StunTimer > 0):
            self.StunTimer -= UpdateEvent.Dt
        if(self.StunTimer <= 0):
            self.StunState = False
            self.StunTimer = 0
            
        #if enemy is not currently stunned
        if(self.StunState == False):
            
            #target is not within range
            targetIsWithinRange = False
            #object name is goblin (can't grapple to it)
            self.Owner.Name = ("Goblin")
            
            #Logic for updating distance from target and chase direction 
            self.CalculateChaseDirectionAndDistance()
            #Determines whether or not to chase of pace 
            targetIsWithinRange = (self.DistanceFromTarget <= self.ChaseTriggerDistance)
            reachMaxRange = (self.DistanceFromHome >= self.MaxMoveDistance)
            
            #If valid object and target is within range 
            if(targetIsWithinRange and self.AfterAttack == False):
                #Chase player
                if(reachMaxRange):
                    self.AfterAttack = True
                else:
                    self.alerted = True
                    self.HomeQ = False
                    self.ChaseTarget(UpdateEvent)
            #if target is not in range
            else:
                #if object currently isn't in starting place
                if(self.HomeQ == False):
                    #run go home function
                    self.GoHome()
                #if enemy is in starting place
                else:
                    #make sure enemy is not green(grapple)
                    self.Owner.Sprite.Color = self.OriginalColor
                    #Run logic for pacing back and forth
                    self.PaceBackAndForth(UpdateEvent)
            
            #Logic for pacing back and forth 
            self.PaceBackAndForth(UpdateEvent)
            
        #if enemy is stunned
        if(self.StunState == True):
            #run stun logic
            self.StunLogic()
            #change color to green(grapple)
            self.Owner.Sprite.Color = Color.Green
            #change object name so player can grapple to enemy
            self.Owner.Name = ("Floor")
            #enemy is not chasing player
            self.alerted = False
            
        #Logic for playing stun sound effect
        if(UpdateEvent.CurrentTime > self.nextPing):
            self.nextPing = UpdateEvent.CurrentTime + self.stunDelay
            if(self.StunState == True):
                self.Space.SoundSpace.PlayCue("stun")
        
    def GoHome(self):
        #Function to move back to starting position
        
        #vector
        direction = (self.StartPosition - self.Owner.Transform.Translation)
        
        #Once enemy is close to starting position
        if(direction.length() <= 0.5):
            #enemy is at starting position
            self.HomeQ = True
            #enemy is not attacking
            self.AfterAttack = False
            self.alerted = False
            
        #move enemy along the normalized vector
        direction.normalize()
        self.Owner.Transform.Translation += direction * 0.25
        
    def PaceBackAndForth(self, UpdateEvent):
        #Logic for pacing/speed while not chasing player

        #How far from starting position 
        displacement = self.Owner.Transform.Translation - self.StartPosition
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
        #Logic for chasing player
        
        #Set Chase Color 
        self.Owner.Sprite.Color = self.ChaseColor
        #Apply movement 
        self.Owner.Transform.Translation += self.ChaseDirection * UpdateEvent.Dt * self.ChaseSpeed
            
    def CalculateChaseDirectionAndDistance(self):
        #Logic for chasing player
        
        #setting player as target
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
        
    def StunLogic(self):
#----------------------------------------------------------------------------------------------------
#Creates number visuals in gameto represent how long an enemy will be stunned for

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
            False
            
#----------------------------------------------------------------------------------------------------
        
    def OnCollisionStart(self, CollisionEvent):
        #Logic for enemy colliding with player or weapon projectile
        
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            #enemy is being stunned by player
            self.StunState = True
            #set stun counter
            self.StunTimer = 5
            
        if(CollisionEvent.OtherObject.Name == "Player"):
            #enemy is attacking player
            self.AfterAttack = True


Zero.RegisterComponent("GoblinEnemy", GoblinEnemy)