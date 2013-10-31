import Zero
import Events
import Property
import VectorMath

class TextFollow:
    def Initialize(self, initializer):
        #Connect to LogicUpdate event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        
    def OnLogicUpdate(self, UpdateEvent):
        self.targetObject = self.Space.FindObjectByName("Camera")
        if(self.targetObject):
        #Get our current translation
            currentTranslation = self.Owner.Transform.Translation
        #Get target object's translation
            targetTranslation = self.targetObject.Transform.Translation
        #Use x component of target translation with our y and z translation
            newTranslation = VectorMath.Vec3(targetTranslation.x - 10, -10.5, currentTranslation.z)
        #Update our translation with the new translation
            self.Owner.Transform.Translation = newTranslation

Zero.RegisterComponent("TextFollow", TextFollow)