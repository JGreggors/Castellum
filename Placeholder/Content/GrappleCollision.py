import Zero
import Events
import Property
import VectorMath
import Color

class GrappleCollision:
#Apply to objects that you DON"T want Grapple to grapple to
#Changes color of cursor
    def Initialize(self, initializer):
        Zero.Connect(self.Owner, Events.MouseEnter, self.OnMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.OnMouseExit)
        self.reticle = self.Space.FindObjectByName("Target")
        
    def OnMouseEnter(self, MouseEvent):
        self.reticle.Sprite.Color = Color.Red

    def OnMouseExit(self, MouseEvent):
        self.reticle.Sprite.Color = Color.Yellow
        
Zero.RegisterComponent("GrappleCollision", GrappleCollision)