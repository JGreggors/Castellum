########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import math
import Color

#Creating a shortcut for VectorMath.Vec3
Vec3 = VectorMath.Vec3

class MasterPlayerContr:
    
    #variables for character movement
    moveSpeed = Property.Float(10.0)
    jumpHeight = Property.Float(2.0)
    #variables for weapon
    ShootSpeed = Property.Float(5.0)
    Overheat = Property.Float(150.0)
    CooldownSpeed = Property.Int(50)
    
    def Initialize(self, initializer):

        #Creating LogicUpdate, CollisionStarted
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStarted)
        
#----------------------------------------------------------
#Player Movement Related:
        
        #creating varaible for player arm
        self.arm = self.Owner.FindChildByName("arm")
        #Setting starting ground state
        self.OnGround = False
        #Setting starting player direction
        self.playerDirection = False
        self.moveRight = False
        self.moveLeft = False
        self.jumpIsPressed = False
        #For key events
        Zero.Connect(Zero.Keyboard, Events.KeyDown, self.OnKeyDown)
        Zero.Connect(Zero.Keyboard, Events.KeyUp, self.OnKeyUp)
        
#----------------------------------------------------------
#for gold (gems) count

        self.gold = 0
        
#----------------------------------------------------------
#Grappling Hook Related: 
    
        #Variable for camera
        cameraCog = self.Space.FindObjectByName("Camera")
        #Mouse Events
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseMove, self.OnMouseMove)
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseUpdate, self.OnMouseUpdate)
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseUp, self.OnMouseUp)
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseDown, self.OnMouseDown)
        #Variables for calculations
        self.playerGrappleShot = False
        self.grappleDistance = 0
        self.grappleHit = 0
        self.grapplePoint = Vec3(0,0,0)
        self.Grapple = 0
        self.hook = 0
        self.Swing = False
        self.swingDown = True
        self.mousePosition = VectorMath.Vec3(0,0,0)

#----------------------------------------------------------
#Shooting

        #Mouse event for shooting
        Zero.Connect(self.Space, Events.RightMouseDown, self.OnRightClick)
        self.Heat = 0.0
        self.CanShoot = True
        self.Shoot = 0.0
        self.spaceIsPressed = False
        self.ResetIsPressed = False

#----------------------------------------------------------
#Key object related

        self.keyAttached = False
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
        #Stops a grapple if there was one already
        self.StopGrapple()
        #Changes arm sprite source
        self.Owner.FindChildByName("arm").Sprite.SpriteSource = "armfired"
        
        #telling that the player is shooting grappling hook
        self.playerGrappleShot = True
        #making a variable that is the same as MouseDirection variable
        direction = self.MouseDirection
        direction = math.atan2(direction.y, direction.x)
        #direction of making a variable into where mousePosition is
        self.grappleDirectionPoint = self.mousePosition
        
        #Grappling 'Rope' object and 'poof' effect
        if(self.Space.CurrentLevel.Name != "MainMenu"):
            self.Grapple = self.Space.CreateAtPosition("Rope", VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .5), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .5) + .15, 0) )
            self.Space.CreateAtPosition("Poof", VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * 1), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * 1) + .15, 0) )
            #Grappling 'Hook' object
            self.hook = self.Space.CreateAtPosition("Hook", VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .5), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .5) + .15, 0) )
        
        self.grappleDirection = self.MouseDirection
        
#----------------------------------------------------------
#Shooting:
    
    def OnRightClick(self, ViewportMouseEvent):
        # if you can't shoot it makes a sound effect
        if(self.CanShoot == False):
            self.Space.SoundSpace.PlayCue("Overheat")
            
        else:
            #plays sound effect
            self.Space.SoundSpace.PlayCue("gunsound1")
            #Adds heat
            self.Heat += 50.0
            #Assigns Shooting projectile
            Shoot = self.Space.CreateAtPosition("Projectile", VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .5), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .5) + .15, 0) )
            #Assigns Shoot direction
            Shoot.Projectile.Direction = self.mousePosition - VectorMath.Vec3(self.Owner.Transform.Translation.x + (math.cos(self.PointDirection) * .5), self.Owner.Transform.Translation.y + (math.sin(self.PointDirection) * .5) + .15, 0) 
            #Normalizes speed
            Shoot.Projectile.Direction = Vec3(Shoot.Projectile.Direction.x / Shoot.Projectile.Direction.length(), Shoot.Projectile.Direction.y / Shoot.Projectile.Direction.length(), 0) * self.ShootSpeed

#----------------------------------------------------------

    def OnMouseUp(self, ViewportMouseEvent):
        #if mouse is not being held and the grapple didn't hit anything stop grapple
        self.MouseDown = False
        if(self.grappleHit == 0):
            self.StopGrapple()
            
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Player Key Input:
    
    def OnKeyDown(self, KeyboardEvent):
        
        #Right
        if(KeyboardEvent.Key == Zero.Keys.A):
            self.moveLeft = True
        #Left
        if(KeyboardEvent.Key == Zero.Keys.D):
            self.moveRight = True
        #Jump
        if(KeyboardEvent.Key == Zero.Keys.Space):
            self.jumpIsPressed = True
        #Reset
        if(KeyboardEvent.Key == Zero.Keys.R):
            self.ResetIsPressed = True

    def OnKeyUp(self, KeyboardEvent):
        
        #Right
        if(KeyboardEvent.Key == Zero.Keys.A):
            self.moveLeft = False
        #Left
        if(KeyboardEvent.Key == Zero.Keys.D):
            self.moveRight = False
        #Jump
        if(KeyboardEvent.Key == Zero.Keys.Space):
            self.jumpIsPressed = False
            self.StopGrapple()
        #Reset
        if(KeyboardEvent.Key == Zero.Keys.R):
            self.ResetIsPressed = False
            
#--------------------------------------------------------------------------------------------

    def OnLogicUpdate(self, UpdateEvent):
        
        #don't use the grapple for animated character on main menu
        if(self.Space.CurrentLevel.Name == "MainMenu"):
            self.StopGrapple()
            
        #run the functions for movement. checking for groun and jumping    
        self.ApplyMovement()
        self.UpdateGroundState()
        self.ApplyJumping()
        
        #flip sprite based on the direction it is moving in
        self.Owner.Sprite.FlipX = self.playerDirection

        #if the player has picked up a key place it above players head
        if(self.keyAttached):
            self.Key.Transform.Translation = self.Owner.Transform.Translation + Vec3(0,.6 * self.Owner.Transform.Scale.y,.1)
            
        #if the game is reset destroy HUD and then relaod level
        if(self.ResetIsPressed == True):
            if(not Zero.Game.FindSpaceByName("HUDSpace")):
                pass
            else:
                Zero.Game.FindSpaceByName("HUDSpace").Destroy()
            self.Space.ReloadLevel()
            
#----------------------------------------------------------
#Used for counting gold

        hudSpace = Zero.Game.FindSpaceByName("HUDSpace")
        if(not hudSpace):
            pass
        else:
            goldObject = hudSpace.FindObjectByName("GCounter")
        
        #Update gold/gem counter on the HUD
            if(goldObject):
                goldObject.SpriteText.Text = str(self.gold)

#----------------------------------------------------------
#Grappling Hook Related:
    
        self.DeltaTime = UpdateEvent.Dt
        #loop through grapple if below is True
        if(self.playerGrappleShot):
           self.CastRayGrapple()
           
        #Setting to a vector
        self.MouseDirection = self.mousePosition - self.Owner.Transform.Translation
        self.PointDirection = math.atan2(self.MouseDirection.y, self.MouseDirection.x)
        self.MouseDirection.normalize()
        #Setting arm movement
        if(self.arm):
            self.arm.Transform.Rotation = VectorMath.Quat(0,0, self.PointDirection + math.radians(45))

#----------------------------------------------------------

#----------------------------------------------------------
#Weapon Overheating/Cool down
 
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
#Pendulum Swing for Grappling Hook
#Uses normals/triangles to calculate next position in swing (faking physics)

    def swingPlayer(self, ray):
        
        #For Swinging Right
        if(self.swingRight and self.swingDown):
            self.Pendulum = VectorMath.Vec3(math.fabs(ray.y), -math.fabs(ray.x), 0)
            #setting swing speeds
            self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 18)
            if(ray.x < 0):
                self.swingDown = False
        elif(self.swingRight and not self.swingDown):
            self.Pendulum = VectorMath.Vec3(math.fabs(ray.y), math.fabs(ray.x), 0)
            #setting swing speeds
            self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 18)
            #when have reached the same height swing started at after swing stop
            if(self.Owner.Transform.Translation.y > self.rayY):
                self.StopGrapple()
                self.swingDown = True
                self.Swing = False
                
       #For Swinging Left
        elif(not self.swingRight and self.swingDown):
            self.Pendulum = VectorMath.Vec3(-math.fabs(ray.y), -math.fabs(ray.x), 0)
            #setting swing speeds
            self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 18)
            if(ray.x > 0):
                self.swingDown = False
        elif(not self.swingRight and not self.swingDown):
            self.Pendulum = VectorMath.Vec3(-math.fabs(ray.y), math.fabs(ray.x), 0)
            #setting swing speeds
            self.Owner.Transform.Translation += self.Pendulum * (self.DeltaTime * 18)
            #when have reached the same height swing started at after swing stop
            if(self.Owner.Transform.Translation.y > self.rayY):
                self.StopGrapple()
                self.swingDown = True
                self.Swing = False
                
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Casting Grappling Hook:
    
    def CastRayGrapple(self):
        
        #creating a ray
        ray = VectorMath.Ray()
        
        #Testing if grapple has hit anything
        if(self.grappleHit == 0):
            direction = self.grappleDirection
        #if yes setting direction to where grapple is and player
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
            self.grappleDistance += self.DeltaTime * 25
        else:
            #distance formula
            self.grappleDistance = math.sqrt(math.pow((ray.Start.x - self.grapplePoint.x), 2) + math.pow((ray.Start.y - self.grapplePoint.y), 2))
            #setting player to kinematic so player can move with grapple
            self.Owner.RigidBody.Kinematic = True
            #stop grapple when the distance between hook and player is 1
            #fixes stuck in the ceiling  bug
            if(self.grappleDistance < 1):
                self.StopGrapple()
                
#----------------------------------------------------------
#Pendulum Swing Related

            #if not swinging at the time
            if(not self.Swing):
                #if mouse is being held down
                if(self.MouseDown == True):
                   #move speed for player to hook on grapple
                   self.Owner.Transform.Translation += ray.Direction * (self.DeltaTime * 18)
                #if mouse is release
                else:
                    #save the current height
                    self.rayY = self.Owner.Transform.Translation.y
                    #begin to swing
                    self.Swing = True
                    #swing right
                    if(ray.Direction.x > 0):
                        self.swingRight = True
                        self.swingDown = True
                        self.swingPlayer(ray.Direction)
                    #swing left
                    else:
                        self.swingRight = False
                        self.swingDown  = True
                        self.swingPlayer(ray.Direction)
            #keep swinging
            else:
                self.swingPlayer(ray.Direction)
                
#----------------------------------------------------------

        #Adds color to the 'Rope'
        rayColor = VectorMath.Vec4(0.45, 0.15, 0, 1)
        #Finds the range of the first thing grapple collides with
        castResultRange = self.Space.PhysicsSpace.CastRayResults(ray, 50)
        
        #checking if the grapple hit anything
        if (self.grappleHit == 0):
            endPosition = ray.Start + ray.Direction * self.grappleDistance
        else:
            #sets position to grapple hit
            endPosition = self.grapplePoint
            
        for castResult in castResultRange:
            #asking if the it hit a certain named object
            #objects with name floor are able to be grappled to
            if(castResult.ObjectHit.Name == "Floor"):
                #attach to this object
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
                    
            #Prevents grapple from hitting player, key (+ AOE region), gate AOE region, and gold
            elif(castResult.ObjectHit.Name != "Player" and castResult.ObjectHit.Name != "Pit" and castResult.ObjectHit.Name != "Key" and castResult.ObjectHit.Name != "AOE" and castResult.ObjectHit.Name != "GateAOE" and castResult.ObjectHit.Name != "Gold"):
                if(castResult.Distance < self.grappleDistance):
                    self.StopGrapple()
            else:
                pass

        #Scales, Rotates, adds Color, and sets Starting Point of Rope 'Rope'
        self.Grapple.Transform.Scale = Vec3(0.2, (math.sqrt(math.pow((ray.Start.x - endPosition.x), 2) + math.pow((ray.Start.y - endPosition.y), 2)) * 2), 1)
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
#Uses same set up as above (see comments above)

    def CastRayStopGrapple(self):
        
        #setting variable for changeability later
        xvalue = .1
        
        if(self.grappleHit == 1):
            
        #Collider 1
            ray = VectorMath.Ray()
            direction = Vec3(xvalue, -0.5,0)
            direction = math.atan2(direction.y, direction.x)
            ray.Start = self.Owner.Transform.Translation
            ray.Direction = Vec3(xvalue*self.Owner.Transform.Scale.x, -0.5*self.Owner.Transform.Scale.y, 0)
            ray.Direction.normalize()
            maxRayCastDistance = .75
            castResultRange = self.Space.PhysicsSpace.CastRayResults(ray, 1)
            endPosition = ray.Start + ray.Direction * maxRayCastDistance
            for castResult in castResultRange:
                if(castResult.Distance >= maxRayCastDistance):
                    break
                endPosition = castResult.WorldPosition
                if (castResult.ObjectHit.Name == "Floor"):
                    self.StopGrapple()

        #Collider 2
            ray2 = VectorMath.Ray()
            direction = Vec3(xvalue, 0.5,0)
            direction = math.atan2(direction.y, direction.x)
            ray2.Start = self.Owner.Transform.Translation
            ray2.Direction = Vec3(xvalue*self.Owner.Transform.Scale.x, 0.5*self.Owner.Transform.Scale.y, 0)
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

        #Collider 3
            ray3 = VectorMath.Ray()
            direction = Vec3(-xvalue, 0.5,0)
            direction = math.atan2(direction.y, direction.x)
            ray3.Start = self.Owner.Transform.Translation
            ray3.Direction = Vec3(-xvalue*self.Owner.Transform.Scale.x, 0.5*self.Owner.Transform.Scale.y, 0)
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

        #Collider 4
            ray4 = VectorMath.Ray()
            direction = Vec3(-xvalue, -0.5,0)
            direction = math.atan2(direction.y, direction.x)
            ray4.Start = self.Owner.Transform.Translation
            ray4.Direction = Vec3(-xvalue*self.Owner.Transform.Scale.x, -0.5*self.Owner.Transform.Scale.y, 0)
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

#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#GrappleStops and Resets everything

    def StopGrapple(self):

        #Reseting all variables
        self.grappleHit = 0
        self.grappleDistance = 0
        self.playerGrappleShot = False
        self.Owner.RigidBody.Kinematic = False
        self.Swing = False
        
        #setting arm back to original sprite
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
        
        #Setting variables for movement and arm placement
        moveDirection = Vec3(0,0,0)
        currentArmTranslation = self.arm.Transform.Translation
        
        #Right
        if(self.moveRight):
            
            #Checking if on the ground
            if(self.OnGround):
                moveDirection += Vec3(1,0,0)
            else:
                moveDirection += Vec3(.5,0,0)
                
            #setting sprite direction
            self.playerDirection = False
            #if the player wasn't previously moving change the sprite source
            if(self.Owner.Sprite.SpriteSource.Name == "player_stand"):
                self.Owner.Sprite.SpriteSource = "player"
           #offset for the arm when facing right
            self.arm.Transform.Translation = Vec3(-.03, currentArmTranslation.y, currentArmTranslation.z)
        
        #Left
        if(self.moveLeft):
            
            #Checking if on the ground
            if(self.OnGround):
                moveDirection += Vec3(-1,0,0)
            else:
                moveDirection += Vec3(-.5,0,0)
                
            #setting sprite direction
            self.playerDirection = True
            #if the playerwasn't previously moving change the sprite source
            if(self.Owner.Sprite.SpriteSource.Name == "player_stand"):
                self.Owner.Sprite.SpriteSource = "player"
            #offset for the arm when facing left
            self.arm.Transform.Translation = Vec3(.03, currentArmTranslation.y, currentArmTranslation.z)
            
        #if the player is not moving at all use standing sprite
        if(not (self.moveRight or self.moveLeft)):
            self.Owner.Sprite.SpriteSource = "player_stand"
            
        #Using Linear Velocity
        self.Owner.RigidBody.ApplyLinearVelocity(moveDirection * (self.moveSpeed/30))
        
    def ApplyJumping(self):
        
        #If able to jump, jump and play sound effect
        if(self.CanJump() and self.jumpIsPressed):
            self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(0,self.jumpHeight,0))
            self.Space.SoundSpace.PlayCue("jump")
            
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
#Updating Ground proporties for Jumping and Grappling:
    
    def CanJump(self):
        #when on the ground return that player can jump
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
#Object Collision

    def OnCollisionStarted(self, CollisionEvent):
        
        #Setting shortcuts for collision objects
        targetObject = CollisionEvent.OtherObject
        Gob = targetObject.Name == "Goblin"
        Bat = targetObject.Name == "Bat"
        key = self.Space.FindObjectByName("Key")
        otherObject = CollisionEvent.OtherObject
        
        #If player touches a key they pick it ip
        if(otherObject.Name == "AOE" and self.keyAttached == False):
            self.Space.SoundSpace.PlayCue("pickupkey")
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(0, .6  * self.Owner.Transform.Scale.y, 1)
            key.RigidBody.Static = True
            key.BoxCollider.Ghost = True
            self.keyAttached = True
            
        #Setting displacement for when character collides with enemy (bounce back)
        displacementX = targetObject.Transform.Translation.x - self.Owner.Transform.Translation.x
        displacementY = targetObject.Transform.Translation.y - self.Owner.Transform.Translation.y
        
        #Stops grapple if hits objects other than gold, key (+ AOE key region) when swinging
        if(self.Swing and targetObject.Name != "Gold" and targetObject.Name != "Key" and targetObject.Name != "AOE"):
                self.StopGrapple()

#--------------------------------------
#Enemies (bounce back when colliding)

        if(Gob):
            self.Owner.RigidBody.ApplyForce(VectorMath.Vec3((displacementX * -100),(displacementY * -250),0))
            targetObject.RigidBody.ApplyForce(VectorMath.Vec3((displacementX * 250),(displacementY * 50),0))
        if(Bat):
            self.Owner.RigidBody.ApplyForce(VectorMath.Vec3((displacementX * -150),(displacementY * -150),0))
            targetObject.RigidBody.ApplyForce(VectorMath.Vec3((displacementX * 150),(displacementY * 150),0))
            
#--------------------------------------
#Gold/Gem Related

        #If the player collides with a gold/gem object
        if(targetObject.Name == "Gold"):
            #increase gold count
            self.gold += 1
            #play sound effect
            self.Space.SoundSpace.PlayCue("gold")
            
#--------------------------------------
#When the player gets hit by enemy or put while holding key they drop the key

        #"Bat" type enemy
        if(self.keyAttached == True and otherObject.Name == "Bat"):
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(1, 0, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
            key.BoxCollider.Ghost = False
            
        #"Goblin" type enemy
        elif(self.keyAttached == True and otherObject.Name == "Goblin"):
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(1, 0, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
            key.BoxCollider.Ghost = False
            
        #Firepit
        elif(self.keyAttached == True and otherObject.Name == "Pit"):
            key.Transform.Translation = self.Owner.Transform.Translation + Vec3(0, 1, 0)
            key.RigidBody.Static = False
            self.keyAttached = False
            key.BoxCollider.Ghost = False
            
#--------------------------------------------------------------------------------------------

Zero.RegisterComponent("MasterPlayerContr", MasterPlayerContr)