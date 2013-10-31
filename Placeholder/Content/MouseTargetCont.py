import Zero
import Events
import Property
import VectorMath
import Color

class MouseTargetCont:
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        cameraCog = self.Space.FindObjectByName("Camera")
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseMove, self.OnMouseMove)
        Zero.Connect(cameraCog.Camera.Viewport, Events.MouseUpdate, self.OnMouseUpdate)
        self.mousePosition = VectorMath.Vec3(0,0,0)
        Zero.Mouse.Cursor = -1
       
    def OnMouseMove(self, ViewportMouseEvent):
        #finding where the mouse is in the game
        self.mousePosition = ViewportMouseEvent.ToWorldZPlane(0.0)
        
    def OnMouseUpdate(self, ViewportMouseEvent):
        self.mousePosition = ViewportMouseEvent.ToWorldZPlane(0.0)
        
        
    def OnLogicUpdate(self, UpdateEvent):
        currentTranslation = self.Owner.Transform.Translation
        newTranslation = VectorMath.Vec3(self.mousePosition.x, self.mousePosition.y, 0)
        self.Owner.Transform.Translation = newTranslation
        




Zero.RegisterComponent("MouseTargetCont", MouseTargetCont)