import Zero
import Events
import Property
import VectorMath
import Color
import random


class Death:
    alphaTimer = Property.Float(0.001)
    destroyTimer = Property.Int(1000)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
            
    def OnLogicUpdate(self, UpdateEvent):
        #cameraTimer = 15
        randomDirectionX = random.uniform(-3, 3)
        randomDirectionY = random.uniform(1, 2)
        #print(self.destroyTimer)
        #print(self.Owner.Sprite.Color)
        self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(randomDirectionX, randomDirectionY, 0))
        self.Owner.Sprite.Color = self.Owner.Sprite.Color - VectorMath.Vec4(0, 0, 0, self.alphaTimer)
        self.destroyTimer -= 1
        self.Owner.RigidBody.ApplyLinearVelocity(VectorMath.Vec3(0, 0, 0))
        if(self.destroyTimer == 0):
            self.Owner.Destroy()
            
        #cameraTimer -= 1
        #if(cameraTimer <= 0):
        #    self.Space.FindObjectByName("Camera").CameraLogic.targetObject = self.Space.FindObjectByName("Player")

Zero.RegisterComponent("Death", Death)