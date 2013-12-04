import Zero
import Events
import Property
import VectorMath
import os

class VolumeSliderLogic:
    def Initialize(self, initializer):
        
        self.yvalue = -5.5
        
        #Grabs/Creates file, checks if directory exists
        if os.path.exists(Zero.GetUserDirectory() + "Castellum") and os.path.isfile(Zero.GetUserDirectory() + "Castellum\\volume_options.txt"):
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'r+')
            self.percent = int(self.file.readline())
            self.file.close()
        elif os.path.exists(Zero.GetUserDirectory() + "Castellum"):
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'w')
            self.file.write("100")
            self.file.close()
            self.Initialize(initializer)
        else: 
            os.mkdir(Zero.GetUserDirectory() + "Castellum")
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'w')
            self.file.write("100")
            self.file.close()
            self.Initialize(initializer)
        
        self.currentSpace = 0
        #Max left and right movement
        self.x_left = -3.125
        self.x_right = 3.155
        #Total length of movement
        self.total = -self.x_left + self.x_right
        #sets it to what the percent is
        self.Owner.Transform.Translation = VectorMath.Vec3(self.x_left + (self.percent * self.total / 100.0), self.yvalue, -1)
        #finds volume and sets text
        self.volume = self.Space.FindObjectByName("Volume")
        self.volume.SpriteText.Text = "Volume: " + str(round(self.percent)) + "%"
        
        self.clicked = False
        
        cameracog = self.Space.FindObjectByName("Camera")
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
        Zero.Connect(self.Owner, Events.MouseUp, self.onMouseUp)
        Zero.Connect(cameracog.Camera.Viewport, Events.MouseMove, self.onMouseMove)
        Zero.Connect(cameracog.Camera.Viewport, Events.MouseUpdate, self.onMouseUpdate)
        
    def onMouseUpdate(self, ViewportMouseEvent):
        #making sure you can't bring it outside the boundaries of volume menu
        if(self.clicked):
            if(ViewportMouseEvent.ToWorldZPlane(0).x >= self.x_right):
                self.Owner.Transform.Translation = VectorMath.Vec3(self.x_right, self.yvalue, -1)
                self.percent = 100 * (self.Owner.Transform.Translation.x - self.x_left) / self.total
                self.volume.SpriteText.Text = "Volume: " + str(round(self.percent)) + "%"
            elif(ViewportMouseEvent.ToWorldZPlane(0).x <= self.x_left):
                self.Owner.Transform.Translation = VectorMath.Vec3(self.x_left, self.yvalue, -1)
                self.percent = 100 * (self.Owner.Transform.Translation.x - self.x_left) / self.total
                self.volume.SpriteText.Text = "Volume: " + str(round(self.percent)) + "%"
            else:
                self.Owner.Transform.Translation = VectorMath.Vec3(ViewportMouseEvent.ToWorldZPlane(0).x, self.yvalue, -1)
                self.percent = 100 * (self.Owner.Transform.Translation.x - self.x_left) / self.total
                self.volume.SpriteText.Text = "Volume: " + str(round(self.percent)) + "%"
        
    def onMouseMove(self, ViewportMouseEvent):
        #does the same thing as OnMouseUpdate
        if(self.clicked):
            if(ViewportMouseEvent.ToWorldZPlane(0).x >= self.x_right):
                self.Owner.Transform.Translation = VectorMath.Vec3(self.x_right, self.yvalue, -1)
                self.percent = 100 * (self.Owner.Transform.Translation.x - self.x_left) / self.total
                self.volume.SpriteText.Text = "Volume: " + str(round(self.percent)) + "%"
            elif(ViewportMouseEvent.ToWorldZPlane(0).x <= self.x_left):
                self.Owner.Transform.Translation = VectorMath.Vec3(self.x_left, self.yvalue, -1)
                self.percent = 100 * (self.Owner.Transform.Translation.x - self.x_left) / self.total
                self.volume.SpriteText.Text = "Volume: " + str(round(self.percent)) + "%"
            else:
                self.Owner.Transform.Translation = VectorMath.Vec3(ViewportMouseEvent.ToWorldZPlane(0).x, self.yvalue, -1)
                self.percent = 100 * (self.Owner.Transform.Translation.x - self.x_left) / self.total
                self.volume.SpriteText.Text = "Volume: " + str(round(self.percent)) + "%"
        
        
        
    def onMouseDown(self, MouseEvent):
        self.clicked = True
        
    def onMouseUp(self, MouseEvent):
        self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'w')
        self.file.write(str(round(self.percent)))
        self.file.close()

        self.Space.FindObjectByName("LevelSettings").GlobalVolume.setVolume()
        self.clicked = False

Zero.RegisterComponent("VolumeSliderLogic", VolumeSliderLogic)