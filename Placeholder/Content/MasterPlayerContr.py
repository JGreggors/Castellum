import Zero
import Events
import Property
import VectorMath
import math
import Color

Vec3 = VectorMath.Vec3

class MasterPlayerContr:
    
    moveSpeed = Property.Float(10.0)
    jumpHeight = Property.Float(2.0)
    ShootSpeed = Property.Float(5.0)
    Overheat = Property.Float(150.0)
    CooldownSpeed = Property.Int(50)
    
    def Initialize(self, initializer):
        self.arm = self.Owner.FindChildByName("arm")
        #Creating LogicUpdate, CollisionStarted, Collision Persisted (JB)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStarted)
#----------------------------------------------------------
#Player Movement Related:
        #Setting starting ground state
        self.OnGround = False
        #Setting starting player direction
        self.playerDirection = False
        Zero.Connect(Zero.Keyboard, Events.KeyDown, self.OnKeyDown)
        Zero.Connect(Zero.Keyboard, Events.KeyUp, self.OnKeyUp)
        self.moveRight = False
        self.moveLeft = False
        self.jumpIsPressed = False
#----------------------------------------------------------
#Key Related (JB)
        self.keyAttached = False
        self.gold = 0
#----------------------------------------------------------
#Grappling Hook: 
        cameraCog = self.Space.FindObjectByName("Camera")
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseMove, self.OnMouseMove)
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseUpdate, self.OnMouseUpdate)
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseUp, self.OnMouseUp)
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseDown, self.OnMouseDown)
        self.playerGrappleShot = False
        self.grappleDistance = 0
        self.grappleHit = 0
        self.grapplePoint = Vec3(0,0,0)
        self.Grapple = 0
        self.hook = 0
        self.Swing = False
        self.swingDown = True
        self.mousePosition = VectorMath.Vec3(0,0,0)

        self.currentVelocity = 0

#----------------------------------------------------------
#Shooting (JB)
        #For shooting
        Zero.Connect(self.Space, Events.RightMouseDown, self.OnRightClick)
        self.Heat = 0.0
        self.CanShoot = True
        self.Shoot = 0.0
        self.spaceIsPressed = False
        self.ShiftIsPressed = False
        self.EIsPressed = False
        self.RIsPressed = False
#----------------------------------------------------------
        self.Key = self.Space.FindObjectByName("Key")
#--------------------------------------------------------------------------------------------
#Mouse Controls for Grappling Hook/Shooting:
    def OnMouseMove(self, ViewportMouseEvent):
        #Finding position of the mouse in the game
        self.mousePosition = ViewportMouseEvent.ToWorldZPlane(0.0)
        
    def OnMouseUpdate(self, ViewportMouseEvent):
        #Finding position of the mouse in the game
        self.mousePosition = ViewportMouseEvent.ToWorldZPlane(0.0)
        
    def OnMouseDown(self, ViewportMouseEvent):
        #Sets if mouse is being held down
        self.MouseDown = True
        
        #Checks Grapple counter to see if able to grapple
        self.StopGrapple()
        self.Owner.FindChildByName("arm").Sprite.SpriteSource = "armfired"
        self.playerGrappleShot = True
        direction = self.MouseDirection
        direction = math.atan2(direction.y, direction.x)
        self.grappleDirectionPoint = self.mousePosition
        #Grappling 'Rope' object
        if(self.Space.CurrentLevel.Name != "MainMenu"):
            self.Grapple = self.Space.CreateAtPosition("Rope", VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .5), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .5) + .15, 0) )
            self.Space.CreateAtPosition("Poof", VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * 1), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * 1) + .15, 0) )
        #Grappling 'Hook' object
            self.hook = self.Space.CreateAtPosition("Hook", VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .5), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .5) + .15, 0) )
        self.grappleDirection = self.MouseDirection
#----------------------------------------------------------
#Shooting:
    def OnRightClick(self, ViewportMouseEvent):
        # if you can't shoot it makes funny noises
        if(self.CanShoot == False):
            self.Space.SoundSpace.PlayCue("Overheat")
            
        else:
            self.Space.SoundSpace.PlayCue("gunsound1")
            # Adds heat
            self.Heat += 50.0
            #Assigns Shoot
            Shoot = self.Space.CreateAtPosition("Projectile", VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .5), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .5) + .15, 0) )
            #Assigns Shoot direction
            Shoot.Projectile.Direction = self.mousePosition - VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .5), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .5) + .15, 0) 
            #Normalizes speed, sorry its really long. That's what he said.
            Shoot.Projectile.Direction = Vec3(Shoot.Projectile.Direction.x / Shoot.Projectile.Direction.length(), Shoot.Projectile.Direction.y / Shoot.Projectile.Direction.length(), 0) * self.ShootSpeed
#----------------------------------------------------------
    def OnMouseUp(self, ViewportMouseEvent):
        #Sets if mouse is not being held down
        #if(self.Swing == False and self.Grapple == False):
        #    self.Owner.FindChildByName("arm").Sprite.SpriteSource = "arm"
            
        self.MouseDown = False
        if(self.grappleHit == 0):
            self.StopGrapple()
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Player Key Input:
    def OnKeyDown(self, KeyboardEvent):
        if(KeyboardEvent.Key == Zero.Keys.A):
            self.moveLeft = True
        if(KeyboardEvent.Key == Zero.Keys.D):
            self.moveRight = True
        if(KeyboardEvent.Key == Zero.Keys.Space):
            self.jumpIsPressed = True
        #Key Logic (JB)
        if(KeyboardEvent.Key == Zero.Keys.Shift):
            self.ShiftIsPressed = True
            

                
    def OnKeyUp(self, KeyboardEvent):
        if(KeyboardEvent.Key == Zero.Keys.A):
            self.moveLeft = False
        if(KeyboardEvent.Key == Zero.Keys.D):
            self.moveRight = False
        if(KeyboardEvent.Key == Zero.Keys.Space):
            self.jumpIsPressed = False
            self.StopGrapple()
        #Key Logic (JB)
        #if(KeyboardEvent.Key == Zero.Keys.E and self.EIsPressed == True):
        #    if(self.keyAttached):
        #        self.EIsPressed = False
        #if(KeyboardEvent.Key == Zero.Keys.E and self.EIsPressed == False):
        #    if(self.keyAttached):
        #        self.RIsPressed = False
        if(KeyboardEvent.Key == Zero.Keys.Shift):
            self.ShiftIsPressed = False
#--------------------------------------------------------------------------------------------

    def OnLogicUpdate(self, UpdateEvent):
        if(self.Space.CurrentLevel.Name == "MainMenu"):
            self.StopGrapple()
        self.ApplyMovement()
        self.UpdateGroundState()
        self.ApplyJumping()
        self.Owner.Sprite.FlipX = self.playerDirection

        
        if(self.keyAttached):
            self.Key.Transform.Translation = self.Owner.Transform.Translation + Vec3(0,.6 * self.Owner.Transform.Scale.y,0)
            
        if(self.ShiftIsPressed == True):
            if(not Zero.Game.FindSpaceByName("HUDSpace")):
                pass
            else:
                Zero.Game.FindSpaceByName("HUDSpace").Destroy()
            self.Space.ReloadLevel()
#----------------------------------------------------------
#This is for the gold timer, yeah i know. Shut up.
        hudSpace = Zero.Game.FindSpaceByName("HUDSpace")
        if(not hudSpace):
            pass
            
        else:
            
            goldObject = hudSpace.FindObjectByName("GCounter")
        
        #Gold counter
            if(goldObject):
                goldObject.SpriteText.Text = str(self.gold)

#----------------------------------------------------------
#Grappling Hook Related:
        self.DeltaTime = UpdateEvent.Dt
        #loop through grapple if below is True
        if(self.playerGrappleShot):
           self.CastRayGrapple()
        self.MouseDirection = self.mousePosition - self.Owner.Transform.Translation
        self.PointDirection = math.atan2(self.MouseDirection.y, self.MouseDirection.x)
        self.MouseDirection.normalize()
        if(self.arm):
            self.arm.Transform.Rotation = VectorMath.Quat(0,0, self.PointDirection + math.radians(45))
        #Checks ground state for grapple counter
        if(self.OnGround):
            self.grappleCounter = 1
#----------------------------------------------------------

#----------------------------------------------------------
        # Overheat gun Related:
        #Cooldown procedure
        
        # Debug
        #print(self.Heat)
 
            #If there is heat, start cooling down
        if(self.Heat > 0.0):
            self.Heat -= self.CooldownSpeed * UpdateEvent.Dt
        #if heat reaches Zero, stop cooling and allow shooting if you couldn't shoot
        if(self.Heat < 0.0):
            self.Heat = 0.0
            self.CanShoot = True
        #if heat excedes Overheat threshold, you can't shoot.
        if(self.Heat >= self.Overheat):
            self.Heat = self.Overheat
            self.CanShoot = False
            

#----------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Pendulum for Grappling Hook
    def swingPlayer(self, ray):
        if(self.swingRight and self.swingDown):
            self.Pendulum = VectorMath.Vec3(math.fabs(ray.y), -math.fabs(ray.x), 0)
            if(self.Space.CurrentLevel.Name == "InfiniteGrap"):
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 14)
            elif(self.Space.CurrentLevel.Name == "Level13"):
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 12)
            else:
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 18)
            if(ray.x < 0):
                self.swingDown = False
        elif(self.swingRight and not self.swingDown):
            self.Pendulum = VectorMath.Vec3(math.fabs(ray.y), math.fabs(ray.x), 0)
            if(self.Space.CurrentLevel.Name == "InfiniteGrap"):
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 14)
            elif(self.Space.CurrentLevel.Name == "Level13"):
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 12)
            else:
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 18)
            if(self.Owner.Transform.Translation.y > self.rayY):
                #print("STOP GRAPPLE")
                self.StopGrapple()
                self.swingDown = True
                self.Swing = False
        elif(not self.swingRight and self.swingDown):
            self.Pendulum = VectorMath.Vec3(-math.fabs(ray.y), -math.fabs(ray.x), 0)
            if(self.Space.CurrentLevel.Name == "InfiniteGrap"):
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 14)
            elif(self.Space.CurrentLevel.Name == "Level13"):
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 12)
            else:
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 18)
            if(ray.x > 0):
                self.swingDown = False
        elif(not self.swingRight and not self.swingDown):
            self.Pendulum = VectorMath.Vec3(-math.fabs(ray.y), math.fabs(ray.x), 0)
            if(self.Space.CurrentLevel.Name == "InfiniteGrap"):
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 14)
            elif(self.Space.CurrentLevel.Name == "Level13"):
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 12)
            else:
                self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 18)
            if(self.Owner.Transform.Translation.y > self.rayY):
                self.StopGrapple()
                #print("STOP GRAPPLE")
                self.swingDown = True
                self.Swing = False
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Casting Grappling Hook:
    def CastRayGrapple(self):
        ray = VectorMath.Ray()
        #Testing if grapple has hit anything
        if(self.grappleHit == 0):
            direction = self.grappleDirection
        else:
            direction = self.grapplePoint - VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .37*self.Owner.Transform.Scale.x), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .4*self.Owner.Transform.Scale.y) + .15, 0) 

        #Calculating vector for grapple
        direction.normalize()
        ray.Direction = direction
        ray.Direction.normalize()
        direction = math.atan2(direction.y, direction.x)
        
        #Setting starting point at player (can adjust if needed)
        ray.Start = VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .37*self.Owner.Transform.Scale.x), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .4*self.Owner.Transform.Scale.y) + .15, 0) 
        #Increase grapple length if nothing has been hit
        if(self.grappleHit == 0):
            #Grapple speed (can be adjusted if needed)
            if(self.Space.CurrentLevel.Name == "InfiniteGrap"):
                self.grappleDistance += self.DeltaTime * 25
            elif(self.Space.CurrentLevel.Name == "Level13"):
                self.grappleDistance += self.DeltaTime * 14
            else:
                #Grapple speed (can be adjusted if needed)
                self.grappleDistance += self.DeltaTime * 25
        else:
            self.grappleDistance = math.sqrt(math.pow((ray.Start.x - self.grapplePoint.x), 2) + math.pow((ray.Start.y - self.grapplePoint.y), 2))
            self.currentVelocity = self.Owner.RigidBody.Velocity.x
            #print(self.currentVelocity)
            #print("Before")
            self.Owner.RigidBody.Kinematic = True
            if(self.grappleDistance < 1):
                self.StopGrapple()
                
            
#----------------------------------------------------------
#Pendulum Related
            if(not self.Swing):
                if(self.MouseDown == True):
                    if(self.Space.CurrentLevel.Name == "InfiniteGrap"):
                        self.Owner.Transform.Translation += ray.Direction * (self.DeltaTime * 16)
                    elif(self.Space.CurrentLevel.Name == "Level13"):
                        self.Owner.Transform.Translation += ray.Direction * (self.DeltaTime * 14)
                    else:
                        self.Owner.Transform.Translation += ray.Direction * (self.DeltaTime * 18)
                else:
                    #self.Space.SoundSpace.PlayCue("swing")
                    self.rayY = self.Owner.Transform.Translation.y
                    self.Swing = True
                    if(ray.Direction.x > 0):
                        self.swingRight = True
                        #print("RIGHT")
                        self.swingDown = True
                        self.swingPlayer(ray.Direction)
                        
                    else:
                        self.swingRight = False
                        #print("LEFT")
                        self.swingDown  = True
                        self.swingPlayer(ray.Direction)
            else:
                #self.Space.SoundSpace.PlayCue("swing")
                self.swingPlayer(ray.Direction)
#----------------------------------------------------------
  
                           
        #Adds color to the 'Rope'
        rayColor = VectorMath.Vec4(0.45, 0.15, 0, 1)
        #Finds the range of the first thing grapple collides with
        castResultRange = self.Space.PhysicsSpace.CastRayResults(ray, 50)
        if (self.grappleHit == 0):
            endPosition = ray.Start + ray.Direction * self.grappleDistance
        else:
            endPosition = self.grapplePoint
        for castResult in castResultRange:
            #print(castResult.ObjectHit.Name)
            #asking if the it hit a certain named object
            if(castResult.ObjectHit.Name == "Floor"):
                if(castResult.Distance >= self.grappleDistance):
                    break
                #setting endPosition to where it hit
                endPosition = castResult.WorldPosition
                #has it hit anything yet
                if (self.grappleHit == 0):
                    #change it to one if it hit something
                    self.grappleHit = 1
                    #sets grapplePoint to end position so where it hit something
                    self.grapplePoint = endPosition
                    self.Space.SoundSpace.PlayCue("hooked")
            #Prevents grapple from hitting player and the key
            elif(castResult.ObjectHit.Name != "Player" and castResult.ObjectHit.Name != "Pit" and castResult.ObjectHit.Name != "Key" and castResult.ObjectHit.Name != "AOE" and castResult.ObjectHit.Name != "GateAOE" and castResult.ObjectHit.Name != "GWall" and castResult.ObjectHit.Name != "Gold" and castResult.ObjectHit.Name != "Checkpoint"):
                if(castResult.Distance < self.grappleDistance):
                    self.StopGrapple()
            else:
                pass
                #print("whatever")
            
        #Scales, Rotates, adds Color, and sets Starting Point of Rope 'Rope'
        self.Grapple.Transform.Scale = Vec3(0.1, (math.sqrt(math.pow((ray.Start.x - endPosition.x), 2) + math.pow((ray.Start.y - endPosition.y), 2)) * 2), 1)
        self.Grapple.Transform.Rotation = VectorMath.Quat(0,0,direction + math.radians(-90))
        self.Grapple.Transform.Translation = ray.Start
        self.Grapple.Sprite.Color = rayColor
        
        #Setting a 'Hook' at end of the grapple
        self.hook.Transform.Translation = ray.Start + ray.Direction * self.grappleDistance
        self.hook.Transform.Rotation = VectorMath.Quat(0,0,direction + math.radians(-90))
        #fixed collisions: whenever grapple is running run this script as well
        self.CastRayStopGrapple()
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Stops Grapple if player bumps into anything using colliders:
    def CastRayStopGrapple(self):

        if(self.grappleHit == 1):
        #Collider 1
            ray = VectorMath.Ray()
            direction = Vec3(0.5, -0.5,0)
            direction = math.atan2(direction.y, direction.x)
            ray.Start = self.Owner.Transform.Translation
            ray.Direction = Vec3(0.5*self.Owner.Transform.Scale.x, -0.5*self.Owner.Transform.Scale.y, 0)
            ray.Direction.normalize()
            maxRayCastDistance = .75
            castResultRange = self.Space.PhysicsSpace.CastRayResults(ray, 1)
            endPosition = ray.Start + ray.Direction * maxRayCastDistance
            for castResult in castResultRange:
                if(castResult.Distance >= maxRayCastDistance):
                    break
                endPosition = castResult.WorldPosition
                if (castResult.ObjectHit.Name == "Floor"):
                    #code for stopping grapple
                    self.StopGrapple()

            #DebugDraw.DrawSphere(ray.Start + ray.Direction * maxRayCastDistance, 0.25)
        #Collider 2
            ray2 = VectorMath.Ray()
            direction = Vec3(0.5, 0.5,0)
            direction = math.atan2(direction.y, direction.x)
            ray2.Start = self.Owner.Transform.Translation
            ray2.Direction = Vec3(0.5*self.Owner.Transform.Scale.x, 0.5*self.Owner.Transform.Scale.y, 0)
            ray2.Direction.normalize()
            maxRayCastDistance = .75 
            castResultRange = self.Space.PhysicsSpace.CastRayResults(ray2, 1)
            endPosition = ray2.Start + ray2.Direction * maxRayCastDistance
            for castResult in castResultRange:
                if(castResult.Distance >= maxRayCastDistance):
                    break
                endPosition = castResult.WorldPosition
                if (castResult.ObjectHit.Name == "Floor"):
                    self.StopGrapple()

            #DebugDraw.DrawSphere(ray2.Start + ray2.Direction * maxRayCastDistance, 0.25)
        #Collider 3
            ray3 = VectorMath.Ray()
            direction = Vec3(-0.5, 0.5,0)
            direction = math.atan2(direction.y, direction.x)
            ray3.Start = self.Owner.Transform.Translation
            ray3.Direction = Vec3(-0.5*self.Owner.Transform.Scale.x, 0.5*self.Owner.Transform.Scale.y, 0)
            ray3.Direction.normalize()
            maxRayCastDistance = .75
            castResultRange = self.Space.PhysicsSpace.CastRayResults(ray3, 1)
            endPosition = ray3.Start + ray3.Direction * maxRayCastDistance
            for castResult in castResultRange:
                if(castResult.Distance >= maxRayCastDistance):
                    break
                endPosition = castResult.WorldPosition
                if (castResult.ObjectHit.Name == "Floor"):
                    self.StopGrapple()

            #DebugDraw.DrawSphere(ray3.Start + ray3.Direction * maxRayCastDistance, 0.25)
        #Collider 4
            ray4 = VectorMath.Ray()
            direction = Vec3(-0.5, -0.5,0)
            direction = math.atan2(direction.y, direction.x)
            ray4.Start = self.Owner.Transform.Translation
            ray4.Direction = Vec3(-0.5*self.Owner.Transform.Scale.x, -0.5*self.Owner.Transform.Scale.y, 0)
            ray4.Direction.normalize()
            maxRayCastDistance = .75 
            castResultRange = self.Space.PhysicsSpace.CastRayResults(ray4, 1)
            endPosition = ray4.Start + ray4.Direction * maxRayCastDistance
            for castResult in castResultRange:
                if(castResult.Distance >= maxRayCastDistance):
                    break
                endPosition = castResult.WorldPosition
                if (castResult.ObjectHit.Name == "Floor"):
                    self.StopGrapple()
            #DebugDraw.DrawSphere(ray4.Start + ray4.Direction * maxRayCastDistance, 0.25)
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#GrappleStops and Resets everything
    def StopGrapple(self):

        self.grappleHit = 0
        self.grappleDistance = 0
        self.playerGrappleShot = False
        self.Owner.RigidBody.Kinematic = False
        self.Owner.RigidBody.Velocity.x = self.currentVelocity
        #print(self.currentVelocity)
        self.Swing = False
        self.Owner.FindChildByName("arm").Sprite.SpriteSource = "arm"
        #if there is a grapple or hook destroy it
        if(self.Grapple):
            self.Grapple.Destroy()
        if(self.hook):
            self.hook.Destroy()
        
#--------------------------------------------------------------------------------------------
           
#--------------------------------------------------------------------------------------------
#Applying Movement and Jumping 
    def ApplyMovement(self):
        moveDirection = Vec3(0,0,0)
        currentArmTranslation = self.arm.Transform.Translation
        if(self.moveRight):
            if(self.OnGround):
                moveDirection += Vec3(1,0,0)
            else:
                moveDirection += Vec3(.5,0,0)
            self.playerDirection = False
            if(self.Owner.Sprite.SpriteSource.Name == "player_stand"):
                self.Owner.Sprite.SpriteSource = "player"

           
            self.arm.Transform.Translation = Vec3(-.03, currentArmTranslation.y, currentArmTranslation.z)
            
        if(self.moveLeft):
            if(self.OnGround):
                moveDirection += Vec3(-1,0,0)
            else:
                moveDirection += Vec3(-.5,0,0)
            self.playerDirection = True
            if(self.Owner.Sprite.SpriteSource.Name == "player_stand"):
                self.Owner.Sprite.SpriteSource = "player"

            self.arm.Transform.Translation = Vec3(.03, currentArmTranslation.y, currentArmTranslation.z)
        if(not (self.moveRight or self.moveLeft)):
            self.Owner.Sprite.SpriteSource = "player_stand"
            
        self.Owner.RigidBody.ApplyLinearVelocity(moveDirection * (self.moveSpeed/30))
        
    def ApplyJumping(self):
        if(self.CanJump() and self.jumpIsPressed):
            #self.Owner.RigidBody.ApplyLinearImpulse(Vec3(0,4,0))
            #Other Jumping Prototypes
            #self.Owner.RigidBody.ApplyLinearImpulse(Vec3(0,1,0) * self.jumpSpeed)
            self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(0,self.jumpHeight,0))
            self.Space.SoundSpace.PlayCue("jump")
            
#----------------------------------------------------------
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Updating Ground proporties for Jumping and Grappling:
    def CanJump(self):
        canJump = self.OnGround
        return canJump
        
    def UpdateGroundState(self):
        self.OnGround = False
        #Testing if objects are 'ground'
        for ContactHolder in self.Owner.Collider.Contacts:
            #Ignore ghost objects
            if(ContactHolder.IsGhost):
                continue
            objectHit = ContactHolder.OtherObject
            surfaceNormal = -ContactHolder.FirstPoint.WorldNormalTowardsOther
            #If the object is considered walkable
            if(self.IsGround(surfaceNormal)):
                self.OnGround = True
                return
               
    def GetDegreeDifference(self, surfaceNormal):
        #Using angles to test if something is 'Ground'
        UpDirection = Vec3(0,1,0)
        cosTheta = surfaceNormal.dot(UpDirection)
        radians = math.acos(cosTheta)
        degrees = math.degrees(radians)
        return degrees
        
    def IsGround(self, surfaceNormal):
        #defines what is ground
        degrees = self.GetDegreeDifference(surfaceNormal)
        return degrees < 60.0
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Object Collision (Jason can add stuff here):
    def OnCollisionStarted(self, CollisionEvent):
        targetObject = CollisionEvent.OtherObject
        Gob = targetObject.Name == "Goblin"
        Bat = targetObject.Name == "Bat"
        
        key = self.Space.FindObjectByName("Key")
        otherObject = CollisionEvent.OtherObject
        
        if(otherObject.Name == "AOE" and self.keyAttached == False):
            self.Space.SoundSpace.PlayCue("pickupkey")
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(0, .6  * self.Owner.Transform.Scale.y, 0)
            key.RigidBody.Static = True
            key.BoxCollider.Ghost = True
            self.keyAttached = True
            
        
        displacementX = targetObject.Transform.Translation.x - self.Owner.Transform.Translation.x
        displacementY = targetObject.Transform.Translation.y - self.Owner.Transform.Translation.y
        #Stops grapple if hits object
        if(self.Swing and targetObject.Name != "Gold"):
            self.StopGrapple()
            
        if(Gob):
            self.Owner.RigidBody.ApplyForce(VectorMath.Vec3((displacementX * -100),(displacementY * -250),0))
            targetObject.RigidBody.ApplyForce(VectorMath.Vec3((displacementX * 250),(displacementY * 50),0))
        if(Bat):
            self.Owner.RigidBody.ApplyForce(VectorMath.Vec3((displacementX * -150),(displacementY * -150),0))
            targetObject.RigidBody.ApplyForce(VectorMath.Vec3((displacementX * 150),(displacementY * 150),0))
        
        if(targetObject.Name == "Gold"):
            self.gold += 1
            self.Space.SoundSpace.PlayCue("gold")
            
        if(self.keyAttached == True and otherObject.Name == "Bat"):
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(1, 0, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
            key.BoxCollider.Ghost = False
        elif(self.keyAttached == True and otherObject.Name == "Goblin"):
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(1, 0, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
            key.BoxCollider.Ghost = False
        elif(self.keyAttached == True and otherObject.Name == "Pit"):
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(0, 1, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
            key.BoxCollider.Ghost = False
#--------------------------------------------------------------------------------------------


Zero.RegisterComponent("MasterPlayerContr", MasterPlayerContr)