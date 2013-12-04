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
            
            if(self.Space.CurrentLevel.Name == "MainMenu" or self.Space.CurrentLevel.Name == "LevelSelect" or self.Space.CurrentLevel.Name == "Credits"):
                newTranslation = currentTranslation
                self.Owner.Transform.Translation = newTranslation
            else:
                #Use x component of target translation with our y and z translation
                newTranslation = VectorMath.Vec3(targetTranslation.x, currentTranslation.y, currentTranslation.z)
                self.Owner.Transform.Translation = newTranslation
            
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.M)):
            self.Space.SoundSpace.Pause = not self.Space.SoundSpace.Pause
            
        self.Space.FindObjectByName("LevelSettings").HUDCreator.BGSpace.FindObjectByName("Camera").Transform.Translation = VectorMath.Vec3(self.Owner.Transform.Translation.x/2, self.Owner.Transform.Translation.y/2, 40)
        
    def onMouseUpdate(self, MouseEvent):
        pass
        #if(MouseEvent.Scroll.y > 0 and not self.Owner.Camera.Size < 10):
        #    self.Owner.Camera.Size -= 1
        #elif(MouseEvent.Scroll.y < 0 and not self.Owner.Camera.Size > 21):
        #    self.Owner.Camera.Size += 1

        
Zero.RegisterComponent("CameraLogic", CameraLogic)