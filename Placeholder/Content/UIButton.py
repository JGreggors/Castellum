import Zero
import Events
import Property
import VectorMath

Vec4 = VectorMath.Vec4

class UIButton:
    #setting defaults for changing color can change in properties
    DefaultColor = Property.Vector4(default = Vec4(1,1,1,1))
    HoverColor = Property.Vector4(default = Vec4(1,1,0,0.25))
    DownColor = Property.Vector4(default = Vec4(1,1,1,0.5))
    
    def Initialize(self, initializer):
        #to make color change when mouse hovers or clicks
        Zero.Connect(self.Owner, Events.MouseEnter, self.OnMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.OnMouseExit)
        Zero.Connect(self.Owner, Events.MouseUp, self.OnMouseUp)
        Zero.Connect(self.Owner, Events.MouseDown, self.OnMouseDown)
        
        self.DefaultState()
        
    def DefaultState(self):
        self.Owner.SpriteText.Color = self.DefaultColor
        
    def HoverState(self):
        self.Owner.SpriteText.Color = self.HoverColor
        
    def DownState(self):
        self.Owner.SpriteText.Color = self.DownColor
        
    def OnMouseEnter(self, ViewportMouseEvent):
        self.HoverState()
        
    def OnMouseExit(self, ViewportMouseEvent):
        self.DefaultState()
        
    def OnMouseUp(self, ViewportMouseEvent):
        self.HoverState()
        #this way when after mouse has clicked can be able to change levels
        clickedUIButtonEvent = Zero.ScriptEvent()
        clickedUIButtonEvent.object = self.Owner
        #sends event for PlayGameButton script
        self.Owner.DispatchEvent("ClickedUIButton", clickedUIButtonEvent)
       
    def OnMouseDown(self, ViewportMouseEvent):
        self.DownState()
        
Zero.RegisterComponent("UIButton", UIButton)