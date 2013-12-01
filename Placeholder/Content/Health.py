import Zero
import Events
import Property
import VectorMath
import Color
import Action
import random

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
        
        self.Phrase = False
        self.maxcount = 2
        self.count = 2
        
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
            
            #Creating a random number
            randPhrase = random.randint(1,3)
            
            self.Owner.Transform.Translation = self.StartPlace
            self.Health = self.MaxHealth
            self.PlayerSpawned = True
            self.DeathByPit = False
            self.Owner.MasterPlayerContr.StopGrapple()
            self.Owner.RigidBody.Velocity = VectorMath.Vec3(0,0,0)
            
            #Based on what the random number is it will do one of these
            if(randPhrase == 1):
                #if a phrase already exists it will destroy the current one 
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount #and reset the count
                #creating a phrase
                self.Space.CreateAtPosition("Phrase1", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                #setting that to phrase object
                self.phrase = self.Space.FindObjectByName("Phrase1")
                #saying there is a phrase
                self.Phrase = True
                    
            elif(randPhrase == 2):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase2", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase2")
                self.Phrase = True
          
            elif(randPhrase == 3):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase3", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase3")
                self.Phrase = True
                  
        if(self.Phrase):
            if(self.count <= 2):
                self.count -= UpdateEvent.Dt
            if(self.count < 0):
                self.count = self.maxcount
                self.phrase.Destroy()
                self.Phrase = False
                self.PhraseCheck = 0
            
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