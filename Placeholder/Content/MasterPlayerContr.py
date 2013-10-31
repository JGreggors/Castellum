import Zero
import Events
import Property
import VectorMath
import math
import Color

Vec3 = VectorMath.Vec3

class MasterPlayerContr:
    
    moveSpeed = Property.Float(10.0)
    jumpSpeed = Property.Float(10.0)
    ShootSpeed = Property.Float(5.0)
    
    def Initialize(self, initializer):
        #Creating LogicUpdate, CollisionStarted, Collision Persisted (JB)
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Zero.Events.CollisionStarted, self.OnCollisionStarted)
        Zero.Connect(self.Owner, Zero.Events.CollisionPersisted, self.OnCollisionPersisted)
        Zero.Connect(self.Owner, Events.CollisionPersisted, self.OnButtonPress)
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
        self.grappleCounter = 1
#----------------------------------------------------------
#Shooting (JB)
        #For shooting
        Zero.Connect(self.Space, Events.RightMouseDown, self.OnRightClick)
        self.Shoot = 0.0
        self.spaceIsPressed = False
        self.shiftIsPressed = False
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
        if(self.grappleCounter > 0):
            self.grappleCounter -= 1
            self.StopGrapple()
            self.playerGrappleShot = True
            direction = self.MouseDirection 
            direction = math.atan2(direction.y, direction.x)
            self.grappleDirectionPoint = self.mousePosition
            #Grappling 'Rope' object
            self.Grapple = self.Space.CreateAtPosition("Rope", self.Owner.Transform.Translation)
            #Grappling 'Hook' object
            self.hook = self.Space.CreateAtPosition("Hook", self.Owner.Transform.Translation)
            self.grappleDirection = self.MouseDirection
#----------------------------------------------------------
#Shooting:
    def OnRightClick(self, ViewportMouseEvent):
        self.Space.SoundSpace.PlayCue("gunsound1")
        #Assigns Shoot
        Shoot = self.Space.CreateAtPosition("Projectile", self.Owner.Transform.Translation)
        #Assigns Shoot direction
        Shoot.Projectile.Direction = self.mousePosition - self.Owner.Transform.Translation
        #Normalizes speed, sorry its really long. That's what he said.
        Shoot.Projectile.Direction = Vec3(Shoot.Projectile.Direction.x / Shoot.Projectile.Direction.length(), Shoot.Projectile.Direction.y / Shoot.Projectile.Direction.length(), 0) * self.ShootSpeed
#----------------------------------------------------------
    def OnMouseUp(self, ViewportMouseEvent):
        #Sets if mouse is not being held down
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
        if(KeyboardEvent.Key == Zero.Keys.R):
            #if(self.keyAttached):
                self.shiftIsPressed = True
        if(KeyboardEvent.Key == Zero.Keys.E):
            #if(self.keyAttached == False):
                self.spaceIsPressed = True
        if(KeyboardEvent.Key == Zero.Keys.Shift):
                self.RIsPressed = True
            

                
    def OnKeyUp(self, KeyboardEvent):
        if(KeyboardEvent.Key == Zero.Keys.A):
            self.moveLeft = False
        if(KeyboardEvent.Key == Zero.Keys.D):
            self.moveRight = False
        if(KeyboardEvent.Key == Zero.Keys.Space):
            self.jumpIsPressed = False
        #Key Logic (JB)
        if(KeyboardEvent.Key == Zero.Keys.R):
            #if(self.keyAttached):
                self.spaceIsPressed = False
                self.shiftIsPressed = False
        if(KeyboardEvent.Key == Zero.Keys.E):
            #if(self.keyAttached == False):
                self.shiftIsPressed = False
                self.spaceIsPressed = False
        if(KeyboardEvent.Key == Zero.Keys.Shift):
                self.RIsPressed = False
#--------------------------------------------------------------------------------------------

    def OnLogicUpdate(self, UpdateEvent):
        self.ApplyMovement()
        self.UpdateGroundState()
        self.ApplyJumping()
        #self.Owner.Sprite.FlipX=self.playerDirection
        
        if(self.keyAttached):
            self.Key.Transform.Translation = self.Owner.Transform.Translation + Vec3(0,1,0)
            
        if(self.RIsPressed == True):
            self.Space.ReloadLevel()

#----------------------------------------------------------
#Grappling Hook Related:
        self.DeltaTime = UpdateEvent.Dt
        #loop through grapple if below is True
        if(self.playerGrappleShot):
           self.CastRayGrapple()
        self.MouseDirection = self.mousePosition - self.Owner.Transform.Translation
        self.PointDirection = math.atan2(self.MouseDirection.y, self.MouseDirection.x)
        self.MouseDirection.normalize()
        #Checks ground state for grapple counter
        if(self.OnGround):
            self.grappleCounter = 1
#----------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Pendulum for Grappling Hook
    def swingPlayer(self, ray):
        if(self.swingRight and self.swingDown):
            self.Pendulum = VectorMath.Vec3(math.fabs(ray.y), -math.fabs(ray.x), 0)
            self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 12)
            if(ray.x < 0):
                self.swingDown = False
        elif(self.swingRight and not self.swingDown):
            self.Pendulum = VectorMath.Vec3(math.fabs(ray.y), math.fabs(ray.x), 0)
            self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 12)
            if(self.Owner.Transform.Translation.y > self.rayY):
                #print("STOP GRAPPLE")
                self.StopGrapple()
                self.swingDown = True
                self.Swing = False
        elif(not self.swingRight and self.swingDown):
            self.Pendulum = VectorMath.Vec3(-math.fabs(ray.y), -math.fabs(ray.x), 0)
            self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 12)
            if(ray.x > 0):
                self.swingDown = False
        elif(not self.swingRight and not self.swingDown):
            self.Pendulum = VectorMath.Vec3(-math.fabs(ray.y), math.fabs(ray.x), 0)
            self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 12)
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
            direction = self.grapplePoint - self.Owner.Transform.Translation

        #Calculating vector for grapple
        direction.normalize()
        ray.Direction = direction
        ray.Direction.normalize()
        direction = math.atan2(direction.y, direction.x)
        #Setting starting point at player (can adjust if needed)
        ray.Start = self.Owner.Transform.Translation
        #Increase grapple length if nothing has been hit
        if(self.grappleHit == 0):
            #Grapple speed (can be adjusted if needed)
            self.grappleDistance += self.DeltaTime * 13
        else:
            self.grappleDistance = math.sqrt(math.pow((ray.Start.x - self.grapplePoint.x), 2) + math.pow((ray.Start.y - self.grapplePoint.y), 2))
            self.Owner.RigidBody.Kinematic = True
            
#----------------------------------------------------------
#Pendulum Related
            if(not self.Swing):
                if(self.MouseDown == True):
                    self.Owner.Transform.Translation += ray.Direction * (self.DeltaTime * 10)
                else:
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
            #Prevents grapple from hitting player and the key
            elif(castResult.ObjectHit.Name != "Player" and castResult.ObjectHit.Name != "Key" and castResult.ObjectHit.Name != "AOE" and castResult.ObjectHit.Name != "GateAOE" and castResult.ObjectHit.Name != "GWall"):
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
            ray.Direction = Vec3(0.5, -0.5, 0)
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
            ray2.Direction = Vec3(0.5, 0.5, 0)
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
            ray3.Direction = Vec3(-0.5, 0.5, 0)
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
            ray4.Direction = Vec3(-0.5, -0.5, 0)
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
        self.Swing = False
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
        if(self.moveRight):
            if(self.OnGround):
                moveDirection += Vec3(1,0,0)
            else:
                moveDirection += Vec3(.5,0,0)
            self.playerDirection = False
        if(self.moveLeft):
            if(self.OnGround):
                moveDirection += Vec3(-1,0,0)
            else:
                moveDirection += Vec3(-.5,0,0)
            self.playerDirection = True

        self.Owner.RigidBody.ApplyLinearVelocity(moveDirection * (self.moveSpeed/30))
        
    def ApplyJumping(self):
        if(self.CanJump() and self.jumpIsPressed):
            #self.Owner.RigidBody.ApplyLinearImpulse(Vec3(0,4,0))
            #Other Jumping Prototypes
            #self.Owner.RigidBody.ApplyLinearImpulse(Vec3(0,1,0) * self.jumpSpeed)
            self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(0,4,0))
            
#----------------------------------------------------------
#Stops Grapple if player jumps:
        if(self.jumpIsPressed):
            self.StopGrapple()
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
        #Stops grapple if hits object
        if(self.Swing):
            self.StopGrapple()
            
        if(targetObject.Name == "Goblin"):
            self.Owner.RigidBody.ApplyForce(VectorMath.Vec3(-300,0,0))
            targetObject.RigidBody.ApplyForce(VectorMath.Vec3(300,0,0))
            
    def OnCollisionPersisted(self, CollisionEvent):
    #    targetObject = CollisionEvent.OtherObject
    #    if(
        pass
            
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#All of the Key Logic (JB)
    def OnButtonPress(self, CollisionEvent):
        otherObject = CollisionEvent.OtherObject
        key = self.Space.FindObjectByName("Key")
        #print(self.keyAttached)
        if(not otherObject):
            return
        
        if(otherObject.Name == "AOE" and self.spaceIsPressed and self.keyAttached == False):
            #key.AttachToRelative(self.Owner)
            
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(0, 1, 0)
            key.RigidBody.Static = True
            self.keyAttached = True
        elif(self.keyAttached == True and self.shiftIsPressed):
            
            #key.Detach()
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(2, 0, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
        elif(self.keyAttached == True and otherObject.Name == "Bat"):
            #key.Detach()
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(1, 0, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
        elif(self.keyAttached == True and otherObject.Name == "Goblin"):
            #key.Detach()
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(1, 0, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
        elif(otherObject.Name == "Gold"):
            self.gold += 1
#--------------------------------------------------------------------------------------------


Zero.RegisterComponent("MasterPlayerContr", MasterPlayerContr)