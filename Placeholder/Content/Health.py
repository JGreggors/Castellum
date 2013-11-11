import Zero
import Events
import Property
import VectorMath
import Color
import Action

class Health:
    
    MaxHealth = Property.Float(default = 150.0)
    PlayerSpawned = False #am I spawned?
    RegenCounter = Property.Int(3) #time before regen starts
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
        self.Health = self.MaxHealth #set current health to max
        self.OriginalColor = self.Owner.Sprite.Color
        self.StartPlace = self.Owner.Transform.Translation
        self.PlayerSpawned = True
        self.RegenStart = 0
        self.totalDeath = 0
        
    def OnLogicUpdate(self, UpdateEvent):
        #debug stuff
       #---------------------------------------
        #
        #print(self.RegenStart)
        #print(self.Health)
       #---------------------------------------
        #Owner's health is full everything is A ok
        if(self.Health == self.MaxHealth):
            self.Owner.Sprite.Color = self.OriginalColor
        #Health is down color orange
        elif(self.Health > 100.0):
            self.Owner.Sprite.Color = Color.Orange
            self.RegenStart += 1 * UpdateEvent.Dt
        #Health is more down color yellow
        elif(self.Health > 50.0):
            self.Owner.Sprite.Color = Color.Yellow
            self.RegenStart += 1 * UpdateEvent.Dt
        #Healht is WAAAAAAAAAAY down color is black
        elif(self.Health > 0.0):
            self.Owner.Sprite.Color = Color.Black
            self.RegenStart += 1 * UpdateEvent.Dt
        #You dead sucka!
        elif(self.Health <= 0.0):
            self.PlayerSpawned = False
            self.totalDeath += 1 
            #print(self.totalDeath)
        #Respawn procedure
        if(self.PlayerSpawned == False):
            self.Space.CreateAtPosition("Death", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y, -5))
            self.Owner.Transform.Translation = self.StartPlace
            self.Health = self.MaxHealth
            self.PlayerSpawned = True
        #if you aren't dead you're fine
        elif(self.PlayerSpawned == True):
                pass
        #regen procedure
        if(self.RegenStart > self.RegenCounter):
            if(self.Health < self.MaxHealth):
                self.Health += 1 ** UpdateEvent.Dt
            else:
                self.RegenStart = 0
                self.Health = self.MaxHealth
        
        if(Zero.Keyboard.KeyIsPressed(Zero.Keys.Nine)):
            self.Health += 1000000000
#--------------------------------------------------------------------
# for death counter
        hudSpace = Zero.Game.FindSpaceByName("HUDSpace")

        if(not hudSpace):
            pass
        
        else:
            
            deathObject = hudSpace.FindObjectByName("DCounter")
        
        #Death Counter
            deathObject.SpriteText.Text = str(self.totalDeath)
                
                
    def OnCollisionStart(self, CollisionEvent):
        #Bats hurt you
        if(CollisionEvent.OtherObject.Name == "Bat"):
            self.Health += -50.0
            self.RegenStart = 0
        #Goblins hurt you
        if(CollisionEvent.OtherObject.Name == "Goblin"):
            self.Health += -50.0
            self.RegenStart = 0
        #Drops into abysses to never be seen or heard from again kill you
        if(CollisionEvent.OtherObject.Name == "Pit"):
            self.Health = -38
           
            
        

Zero.RegisterComponent("Health", Health)