import Zero
import Events
import Property
import VectorMath

Vec3 = VectorMath.Vec3

class smartcamera:
    
    targetObject = Property.Cog()
    horizontalTriggerDistance = Property.Float(5.0)
    verticalTriggerDistance = Property.Float(5.0)
    newTranslation = Vec3(0,0,0)
    smoothMoveSpeed = Property.Float(1.0)
    smoothMovement = Property.Bool(True)
    moveCamera = Property.Bool(True)
    fixedCamera = Property.Bool(True)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        self.newTranslation = self.Owner.Transform.Translation
        
    def OnLogicUpdate(self, UpdateEvent):
        currentTranslation = self.Owner.Transform.Translation
        targetTranslation = self.targetObject.Transform.Translation
        horizontalDistance = targetTranslation.x - currentTranslation.x
        verticalDistance = targetTranslation.y - currentTranslation.x
        followTarget = False
        
        if(horizontalDistance > self.horizontalTriggerDistance):
            followTarget = True
            
        if(horizontalDistance < -self.horizontalTriggerDistance):
            followTarget = True
            
        if(self.fixedCamera == False):
            if(verticalDistance > self.verticalTriggerDistance):
                followTarget = True
                
            if(verticalDistance > -(self.verticalTriggerDistance + 8)):
                followTarget = True
            
        if(self.moveCamera):
            if(followTarget and self.fixedCamera == True):
                self.newTranslation = Vec3(targetTranslation.x, currentTranslation.y, currentTranslation.z)
            elif(followTarget and self.fixedCamera == False):
                self.newTranslation = Vec3(targetTranslation.x, targetTranslation.y + 3, currentTranslation.z)
            if(self.smoothMovement):
                self.Owner.Transform.Translation = currentTranslation.lerp(self.newTranslation, UpdateEvent.Dt * self.smoothMoveSpeed)

            else:
                self.Owner.Transform.Translation = self.newTranslation
        
        

Zero.RegisterComponent("smartcamera", smartcamera)