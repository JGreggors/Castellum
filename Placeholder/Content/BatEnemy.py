########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import random
import math
import Color

#shortcut for VectorMath.Vec3
Vec3 = VectorMath.Vec3

class BatEnemy:
#"Bat" type enemy logic
    
    #Variables
    temp = 0 #stores trajectory    
    #Can change these in properties menu
    maxMoveDistance = Property.Float(5.0)
    ChaseTriggerDistance = Property.Float(7.0)
    ChaseSpeed = Property.Float(5.0)
    PaceLength = Property.Float(50.0)
    PaceSpeed = Property.Float(1.0)
    Stun = Property.Int(5)
    ReturnSpeed = Property.Float(10.0)
    stunDelay = Property.Float(1.0)
    
    #Startiing position
    HomeQ = True
    #Whether enemy is stunned
    StunState = False
    #Is the bat up
    UpQ = False
    
    def Initialize(self, initializer):
        
        #creating Update Event
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
        self.alerted = False
        self.nextPing = 0.0
        
        #Numbers for displaying in game time enemy is stunned
        self.five = False
        self.four = False
        self.three = False
        self.two = False
        self.one = False
        #-----------------------------------------------------------------------------
        
        #Creating a collision event
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
    def OnLogicUpdate(self, UpdateEvent):
        
        #Whether target iswithin range
        targetIsWithinRange = False
        
        #Count down for how long enemy should be stunned
        if(self.StunTimer > 0):
            self.StunTimer -= UpdateEvent.Dt
        if(self.StunTimer <= 0):
            self.StunState = False
            self.StunTimer = 0
                    
        #if enemy is currently stunned
        if(self.StunState):
            #run stun function
            self.StunLogic()
            #change color to green (green = can grapple)
            self.Owner.Sprite.Color = Color.Green
            #change name so that enemy can be grappled to
            self.Owner.Name = ("Floor")
            #enemy is no longer chasing player
            self.alerted = False
        
        #if enemy is not stunned
        else:
            #Logic for updating distance from target and chase direction 
            self.CalculateChaseDirectionAndDistance()
            #Determines whether or not to chase of pace 
            targetIsWithinRange = (self.DistanceFromTarget <= self.ChaseTriggerDistance)
            
            #If valid object and target is within range chase player
            if(targetIsWithinRange and self.AfterAttack == False):
                self.alerted = True #enemy is alerted
                self.HomeQ = False #no longer in home position
                self.ChaseTarget(UpdateEvent) #begin chase logic
            
            #if player is not within range
            else:
                self.alerted = False #enemy is not alerted
                #if enemy is not in starting area
                if(self.HomeQ == False):
                    #if enemy is lower than its normal path
                    if(self.UpQ == False):
                        #run function to make enemy go back up in air
                        self.GoUp(UpdateEvent)
                    #otherwise use function to move to original spot
                    else:
                        self.GoHome(UpdateEvent)
                        
                #if enemy is in the starting area
                else:
                    #make sure enemy color is not green for grapple
                    self.Owner.Sprite.Color = self.OriginalColor
                    #run fuction for pacing
                    self.IdleMovePattern(UpdateEvent)
            #set name to bat so player can't grapple to it
            self.Owner.Name = ("Bat")
            
        #Logic for playing sound effects
        if(UpdateEvent.CurrentTime > self.nextPing):
            self.nextPing = UpdateEvent.CurrentTime + self.stunDelay
            if(self.StunState == True):
                self.Space.SoundSpace.PlayCue("stun")
            if(self.alerted == True):
                self.Space.SoundSpace.PlayCue("alertedenemy")
            
    def GoHome(self, UpdateEvent):
        #Function to move back to starting position
        
        #vector
        direction = (self.StartPosition - self.Owner.Transform.Translation)
        
        #Once enemy is close to starting position
        if(direction.length() <= 0.5):
            #make translation the saved starting position
            self.Owner.Transform.Translation = self.StartPosition
            #set that the enemy is "home"
            self.HomeQ = True
            #enemy is not attacking
            self.AfterAttack = False
            #enemy does not need to move upwards
            self.UpQ = False
            #enemy is not alerted
            self.alerted = False
        
        #move enemy along the normalized vector
        direction.normalize()
        self.Owner.Transform.Translation += direction * UpdateEvent.Dt * self.ReturnSpeed
        
    def IdleMovePattern(self, UpdateEvent):
        
        #Logic for pacing pattern/speed of enemy
        self.Owner.Transform.Translation += Vec3(math.cos(self.temp * 0.75), math.sin(self.temp), 0) * UpdateEvent.Dt * self.PaceLength
        self.temp += 0.15 * self.PaceSpeed
        
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
        
        #If not set UPQ to true, this will make it go home. 
        #Steps for enemy: 1.CHASETARGET 2.GOUP 3.GOHOME
        
        
    def CalculateChaseDirectionAndDistance(self):
        #logic for chasing player
        
        #Get direction towards target 
        self.ChaseDirection = self.player.Transform.Translation - self.Owner.Transform.Translation
        #Get distance from target 
        self.DistanceFromTarget = self.ChaseDirection.length()
        #Only want unit length direction 
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
            
#----------------------------------------------------------------------------------------------------
        
    def OnCollisionStart(self, CollisionEvent):
        #Logic for enemy colliding with player or weapon projectile
        
        if(CollisionEvent.OtherObject.Name == "Player"):
            #enemy is attacking player
            self.AfterAttack = True
        if(CollisionEvent.OtherObject.Name == "Projectile"):
            #enemy is being stunned by player
            self.StunState = True
            #set stun counter
            self.StunTimer = 5


Zero.RegisterComponent("BatEnemy", BatEnemy)