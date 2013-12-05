########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class CameraLogic:
#Logic for Camera to follow player
    
    def Initialize(self, initializer):
        #Connect to LogicUpdate event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
    def OnLogicUpdate(self, UpdateEvent):
        #Define target object as the player
        self.targetObject = self.Space.FindObjectByName("Player")
        
        #If the player exists
        if(self.targetObject):
            #Get cameras current translation
            currentTranslation = self.Owner.Transform.Translation
            #Get players's translation
            targetTranslation = self.targetObject.Transform.Translation
            #Store x component of player translation with camera's current y and z translation
            newTranslation = VectorMath.Vec3(targetTranslation.x, currentTranslation.y, currentTranslation.z)
            #set this to cameras translation
            self.Owner.Transform.Translation = newTranslation
            
        #If M is pressed music will be muted
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.M)):
            #Pauses the Soundspace
            self.Space.SoundSpace.Pause = not self.Space.SoundSpace.Pause
            
        #Sets up the camera for the background so it is slighty off of player movement for effect
        self.Space.FindObjectByName("LevelSettings").HUDCreator.BGSpace.FindObjectByName("Camera").Transform.Translation = VectorMath.Vec3(self.Owner.Transform.Translation.x/2, self.Owner.Transform.Translation.y/2, 40)
        

        
Zero.RegisterComponent("CameraLogic", CameraLogic)