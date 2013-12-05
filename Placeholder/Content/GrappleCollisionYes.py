########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Color 

class GrappleCollisionYes:
#Apply to objects that you want Grapple to grapple to
#Changes color of cursor

    def Initialize(self, initializer):
        
        #Setting up events to check for mouse interacting with object
        Zero.Connect(self.Owner, Events.MouseEnter, self.OnMouseEnter)
        Zero.Connect(self.Owner, Events.MouseExit, self.OnMouseExit)
        
        #setting variable for cursor reticle
        self.reticle = self.Space.FindObjectByName("Target")
        
    def OnMouseEnter(self, MouseEvent):
        
        #Changes color of reticle to green to indicate player can grapple to this object
        self.reticle.Sprite.Color = Color.Green

    def OnMouseExit(self, MouseEvent):
        
        #Changes color of reticle to Yellow when player is no longer hovering over object
        self.reticle.Sprite.Color = Color.Yellow

Zero.RegisterComponent("GrappleCollisionYes", GrappleCollisionYes)