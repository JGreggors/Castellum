########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import os

class VolumeSliderLogic:
    def Initialize(self, initializer):
        
        self.yvalue = -5.5
        
        #Checks if there is a volume text file and creates one if it doesn't exist
        if os.path.exists(Zero.GetUserDirectory() + "Castellum") and os.path.isfile(Zero.GetUserDirectory() + "Castellum\\volume_options.txt"):
            
            #opens file for reading
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'r+')
            #reads in value after converting it to an integer
            self.percent = int(self.file.readline())
            #closes file
            self.file.close()
        
        elif os.path.exists(Zero.GetUserDirectory() + "Castellum"):
            #opens file for writing
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'w')
            #writes to fiile 100 (max volume)
            self.file.write("100")
            #closes file
            self.file.close()
            #re-Intitializes script so we can check to read file
            self.Initialize(initializer)
        
        else: 
            #Creating a file if there wasn't one
            os.mkdir(Zero.GetUserDirectory() + "Castellum")
            self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'w')
            #writes to file 100 (max Volume)
            self.file.write("100")
            #Closes file
            self.file.close()
            #re-Intitializes script so we can check to read file
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
        
        #camera varaible
        cameracog = self.Space.FindObjectByName("Camera")
        
        #setting up mouse events
        Zero.Connect(self.Owner, Events.MouseDown, self.onMouseDown)
        Zero.Connect(self.Owner, Events.MouseUp, self.onMouseUp)
        Zero.Connect(cameracog.Camera.Viewport, Events.MouseMove, self.onMouseMove)
        Zero.Connect(cameracog.Camera.Viewport, Events.MouseUpdate, self.onMouseUpdate)
        
#----------------------------------------------------------------------------------------------------
#making sure you can't bring it outside the boundaries of volume menu

    def onMouseUpdate(self, ViewportMouseEvent):
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

#----------------------------------------------------------------------------------------------------       
        
    def onMouseDown(self, MouseEvent):
        self.clicked = True
        
    def onMouseUp(self, MouseEvent):
        
        #Write the changed volume to file
        self.file = open(Zero.GetUserDirectory() + "Castellum\\" + "volume_options.txt", 'w')
        self.file.write(str(round(self.percent)))
        self.file.close() #closes file
        
        #Tells Global Volume Script to change volume
        self.Space.FindObjectByName("LevelSettings").GlobalVolume.setVolume()
        self.clicked = False

Zero.RegisterComponent("VolumeSliderLogic", VolumeSliderLogic)