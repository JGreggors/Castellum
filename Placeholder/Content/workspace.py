import Zero
import Events
import Property
import VectorMath

class workspace:
    def Initialize(self, initializer):
        targetObject = Property.Cog("Player")
        horizontalMaxDistance = Property.Float(1.0)
        verticalMaxDistance = Property.Float(1.0)
        newTranslation = Vec3(0,0,0)
        smoothMoveSpeed = Property.Float(4.0)
        smoothMovement = Property.Bool(True)
        moveCamera = Property.Bool(True)
        fixedCamera = Property.Bool(True)
        MouseDistance = Property.Float(40.5)
        verticalDistance = Property.Float(35)
        
        def Initialize(self, initializer):
            Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
            self.newTranslation = self.Owner.Transform.Translation
            
            self.PlayerDirection = Vec3(0,0,0)
            self.DistanceFromPlayer = 0.0
            self.HomeY = self.Owner.Transform.Translation.y
            
        def OnLogicUpdate(self, UpdateEvent):
            print(self.DistanceFromPlayer)
            currentTranslation = self.Owner.Transform.Translation
            targetTranslation = self.targetObject.Transform.Translation
            #horizontalDistance = targetTranslation.x - currentTranslation.x
            #verticalDistance = targetTranslation.y - currentTranslation.x
            followTarget = False
            Mouse = self.Space.FindObjectByName("Target").Transform.Translation
            
            self.CalculateMouseDistance()
            #Determines whether or not to chase of pace 
            
            if(self.DistanceFromPlayer <= self.MouseDistance and self.DistanceFromPlayer <= self.verticalDistance):
                self.newTranslation = Vec3(targetTranslation.x, self.HomeY, currentTranslation.z)
                self.Owner.Transform.Translation = self.newTranslation
            elif((self.DistanceFromPlayer >= self.MouseDistance  and self.DistanceFromPlayer <= self.horizontalMaxDistance) and (self.DistanceFromPlayer >= self.verticalDistance and self.DistanceFromPlayer <= self.verticalMaxDistance)):
                self.newTranslation = Vec3(Mouse.x, Mouse.y, currentTranslation.z)
                self.Owner.Transform.Translation = self.newTranslation
            
                
                    
                #if(self.moveCamera):
                #    if(followTarget and self.fixedCamera == True):
                #        self.newTranslation = Vec3(targetTranslation.x, currentTranslation.y, currentTranslation.z)
                #    elif(followTarget and self.fixedCamera == False):
                #        self.newTranslation = Vec3(targetTranslation.x, targetTranslation.y, currentTranslation.z)
                #    if(self.smoothMovement):
                #        self.Owner.Transform.Translation = currentTranslation.lerp(self.newTranslation, UpdateEvent.Dt * self.smoothMoveSpeed)

                #    else:
                #        self.Owner.Transform.Translation = self.newTranslation
                
        def CalculateMouseDistance(self):
            Target = self.Space.FindObjectByName("Target")
            self.MouseDirection = Target.Transform.Translation - self.Owner.Transform.Translation
            #Get distance from target 
            self.DistanceFromPlayer = (self.MouseDirection.length() - 40) * 100
            #Only want unit length direction 
            self.MouseDirection.normalize()
            
            

Zero.RegisterComponent("workspace", workspace)