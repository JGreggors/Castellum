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
    pingDelay = Property.Float(1.0)
    
    def Initialize(self, initializer):
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
        self.Health = self.MaxHealth #set current health to max
        self.OriginalColor = self.Owner.Sprite.Color
        self.StartPlace = self.Owner.Transform.Translation
        self.PlayerSpawned = True
        self.RegenStart = 0
        self.totalDeath = 0
        self.nextPing = 0.0
        
        self.DeathByPit = False
        
        self.hurt = False
        self.hurtmore = False
        self.hurtmost = False
        
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
            self.hurt = False
            self.hurtmore = False
            self.hurtmost = False
        #Health is down color orange
        elif(self.Health >= 100.0):
            self.hurt = True
            self.hurtmore = False
            self.hurtmost = False
            self.Owner.Sprite.Color = Color.Orange
            self.RegenStart += 1 * UpdateEvent.Dt
        #Health is more down color yellow
        elif(self.Health > 50.0):
            self.hurt = False
            self.hurtmore = True
            self.hurtmost = False
            self.Owner.Sprite.Color = Color.Yellow
            self.RegenStart += 1 * UpdateEvent.Dt
        #Healht is WAAAAAAAAAAY down color is black
        elif(self.Health > 0.0):
            self.hurt = False
            self.hurtmore = False
            self.hurtmost = True
            self.Owner.Sprite.Color = Color.Black
            self.RegenStart += 1 * UpdateEvent.Dt
        #You dead sucka!
        elif(self.Health <= 0.0):
            self.hurtmost = False
            self.Space.SoundSpace.PlayCue("death")
            self.PlayerSpawned = False
            self.totalDeath += 1 
            #print(self.totalDeath)
        #Respawn procedure
        if(self.PlayerSpawned == False):
            if(self.DeathByPit == False):
                self.Space.CreateAtPosition("Death", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y, -5))
            self.Owner.Transform.Translation = self.StartPlace
            self.Health = self.MaxHealth
            self.PlayerSpawned = True
            self.DeathByPit = False
            self.Owner.MasterPlayerContr.StopGrapple()
            self.Owner.RigidBody.Velocity = VectorMath.Vec3(0,0,0)
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
            
            
        if(UpdateEvent.CurrentTime > self.nextPing):
            self.nextPing = UpdateEvent.CurrentTime + self.pingDelay
            if(self.hurt == True):
                self.Space.SoundSpace.PlayCue("hurtlittle")
            if(self.hurtmore == True):
                self.Space.SoundSpace.PlayCue("hurtmedium")
            if(self.hurtmost == True):
                self.Space.SoundSpace.PlayCue("hurtmax")

#--------------------------------------------------------------------
# for death counter
        hudSpace = Zero.Game.FindSpaceByName("HUDSpace")

        if(not hudSpace):
            pass
        
        else:
            
            deathObject = hudSpace.FindObjectByName("DCounter")
        
        #Death Counter
            if(deathObject):
                deathObject.SpriteText.Text = str(self.totalDeath)
                
                
    def OnCollisionStart(self, CollisionEvent):
        #Bats hurt you
        if(CollisionEvent.OtherObject.Name == "Bat"):
            self.Health += -50.0
            self.RegenStart = 0
            self.Space.SoundSpace.PlayCue("hit")
        #Goblins hurt you
        if(CollisionEvent.OtherObject.Name == "Goblin"):
            self.Health += -50.0
            self.RegenStart = 0
            self.Space.SoundSpace.PlayCue("hit")
        #Drops into abysses to never be seen or heard from again kill you
        if(CollisionEvent.OtherObject.Name == "Pit"):
            self.DeathByPit = True
            self.Space.CreateAtPosition("Fizzle", self.Owner.Transform.Translation)
            self.Health = -38
           
            
        

Zero.RegisterComponent("Health", Health)