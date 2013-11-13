import Zero
import Events
import Property
import VectorMath

class CameraLogic:

    
    def Initialize(self, initializer):
        #Connect to LogicUpdate event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.MouseUpdate, self.onMouseUpdate)
        
        
    def OnLogicUpdate(self, UpdateEvent):
        self.targetObject = self.Space.FindObjectByName("Player")
        if(self.targetObject):
        #Get our current translation
            currentTranslation = self.Owner.Transform.Translation
        #Get target object's translation
            targetTranslation = self.targetObject.Transform.Translation
        #Use x component of target translation with our y and z translation
            if(self.Space.CurrentLevel.Name == "Level2"):
                if(targetTranslation.y + 3.4 >= 2):
                    newTranslation = VectorMath.Vec3(targetTranslation.x, 2, currentTranslation.z)
                else:
                    newTranslation = VectorMath.Vec3(targetTranslation.x, targetTranslation.y + 3.4, currentTranslation.z)
            #Update our translation with the new translation
            elif(self.Space.CurrentLevel.Name == "InfiniteGrap"):
                newTranslation = VectorMath.Vec3(targetTranslation.x, -5, currentTranslation.z)
            elif(self.Space.CurrentLevel.Name != "Level2"):
                newTranslation = VectorMath.Vec3(targetTranslation.x, targetTranslation.y + 3.4, currentTranslation.z)
            self.Owner.Transform.Translation = newTranslation
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.M)):
            self.Space.SoundSpace.Pause = not self.Space.SoundSpace.Pause
        
    def onMouseUpdate(self, MouseEvent):
        if(MouseEvent.Scroll.y > 0 and not self.Owner.Camera.Size < 10):
            self.Owner.Camera.Size -= 1
        elif(MouseEvent.Scroll.y < 0 and not self.Owner.Camera.Size > 21):
            self.Owner.Camera.Size += 1

        
Zero.RegisterComponent("CameraLogic", CameraLogic)