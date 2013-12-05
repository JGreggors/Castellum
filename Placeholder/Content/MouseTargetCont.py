########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Color

class MouseTargetCont:
#Logic for reticle sprite to follow cursor

    def Initialize(self, initializer):
        #Setting up Update Event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        
        #Creating a variable for camera object
        cameraCog = self.Space.FindObjectByName("Camera")
        
        #Setting up Mouse Related Events
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseMove, self.OnMouseMove)
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseUpdate, self.OnMouseUpdate)
        
        #Setting mouse position to an x,y,z vector
        self.mousePosition = VectorMath.Vec3(0,0,0)
        
        #making Windows cursor invisible
        Zero.Mouse.Cursor = -1
       
#---------------------------------------------------------------------------------------
#Mouse Events find where the mouse is in the game as the mouse updates
    def OnMouseMove(self, ViewportMouseEvent):
        self.mousePosition = ViewportMouseEvent.ToWorldZPlane(0.0)
        currentTranslation = self.Owner.Transform.Translation
        newTranslation = VectorMath.Vec3(self.mousePosition.x, self.mousePosition.y, 30)
        self.Owner.Transform.Translation = newTranslation
        Zero.Mouse.Cursor = -1
        
    def OnMouseUpdate(self, ViewportMouseEvent):
        self.mousePosition = ViewportMouseEvent.ToWorldZPlane(0.0)
        currentTranslation = self.Owner.Transform.Translation
        newTranslation = VectorMath.Vec3(self.mousePosition.x, self.mousePosition.y, 30)
        self.Owner.Transform.Translation = newTranslation
        Zero.Mouse.Cursor = -1
#---------------------------------------------------------------------------------------
        
    def OnLogicUpdate(self, UpdateEvent):
        #Sets the reticle sprite to the translation of the mouse
        currentTranslation = self.Owner.Transform.Translation
        newTranslation = VectorMath.Vec3(self.mousePosition.x, self.mousePosition.y, 30)
        self.Owner.Transform.Translation = newTranslation

Zero.RegisterComponent("MouseTargetCont", MouseTargetCont)