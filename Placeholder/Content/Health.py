########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath
import Color
import Action
import random

class Health:
#Manager for health of player
#Handles respawning as well as insult generator 

    #setting variable so we can change max health later if needed
    MaxHealth = Property.Float(default = 150.0)
    
    #Setting up spawn check
    PlayerSpawned = False
    
    #Variable for time before health starts to regenerate
    RegenCounter = Property.Int(3)
    #Variable for sound cue timers
    pingDelay = Property.Float(1.0)
    
    def Initialize(self, initializer):
        
        #setting up a Logic Update Event
        Zero.Connect(self.Space, Events.LogicUpdate, self.OnLogicUpdate)
        #Setting Up a Collision Event
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        
        #start with health as max health
        self.Health = self.MaxHealth
        #set health bar to original color to start
        self.OriginalColor = self.Owner.Sprite.Color
        #save the starting place of the player
        self.StartPlace = self.Owner.Transform.Translation
        #saying that the player has spawned
        self.PlayerSpawned = True
        
        #setting variable to zero to start
        self.RegenStart = 0
        self.totalDeath = 0
        self.nextPing = 0.0
        
        #setting that the player has not yet been killed by fire pit
        self.DeathByPit = False

        #setting variables for different levels of being hurt
        self.hurt = False
        self.hurtmore = False
        self.hurtmost = False
        
        #setting variables for health bar in HUDSpace
        self.healthbar = self.Space.FindObjectByName("LevelSettings").HUDCreator.HUDSpace.FindObjectByName("Healthbar")
        self.healthbarscalex = self.healthbar.Transform.Scale.x
        
        #setting that a taunting phrase is currently not on the screen
        self.Phrase = False
        #setting up timer variables for how long a phrase should be displayed
        self.maxcount = 2
        self.count = 2
        
    def OnLogicUpdate(self, UpdateEvent):

        #setting a variable for the key
        key = self.Space.FindObjectByName("Key")
        
        #scaling the health bar based on how much health player has
        self.healthbar.Transform.Scale = VectorMath.Vec3((self.Health / self.MaxHealth) * self.healthbarscalex,0.113,1)
        
        #Players health is full: player is not hurt, and the health bar is green
        if(self.Health == self.MaxHealth):
            self.healthbar.Sprite.Color = Color.Green
            self.hurt = False
            self.hurtmore = False
            self.hurtmost = False
            
        #Health is between 100-149: player is hurt, health bar is Yellow, start regen process
        elif(self.Health >= 100.0):
            self.hurt = True
            self.hurtmore = False
            self.hurtmost = False
            self.healthbar.Sprite.Color = Color.Yellow
            self.RegenStart += 1 * UpdateEvent.Dt
            
        #Health is between 50-99: player is hurt more, health bar is red, start regen process
        elif(self.Health >= 50.0):
            self.hurt = False
            self.hurtmore = True
            self.hurtmost = False
            self.healthbar.Sprite.Color = Color.Red
            self.RegenStart += 1 * UpdateEvent.Dt
            
        #Health is between 1-49: player is really hurt, health bar is black, start regen process
        elif(self.Health > 0.0):
            self.hurt = False
            self.hurtmore = False
            self.hurtmost = True
            self.healthbar.Sprite.Color = Color.Black
            self.RegenStart += 1 * UpdateEvent.Dt
        
        #Health is 0 or less: player is dead
        elif(self.Health <= 0.0):
            self.hurtmost = False
            #Play death sound effect
            self.Space.SoundSpace.PlayCue("death")
            #the player is no longer spawned
            self.PlayerSpawned = False
            #increase death count on HUD
            self.totalDeath += 1 
            
            #checks if the player was holding a key
            if(self.Space.FindObjectByName("Player").MasterPlayerContr.keyAttached == True):
                #if so detach key and reset key to original spot with original properties
                self.Space.FindObjectByName("Player").MasterPlayerContr.keyAttached == False
                key.Transform.Translation = self.Owner.Transform.Translation + Vec3(1, 0, 0)
                key.RigidBody.Static = False
                key.BoxCollider.Ghost = False

        #Start respawn procedire since player has died
        if(self.PlayerSpawned == False):
            
            #if the player did not die in fire put create a dead body "object" at position where player died
            if(self.DeathByPit == False):
                self.Space.CreateAtPosition("Death", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y, -5))
            
            #Creating a random number to generate a random insulting phrase
            randPhrase = random.randint(1,34)
            
            #place the player back at starting position
            self.Owner.Transform.Translation = self.StartPlace
            #reset health to maximum value
            self.Health = self.MaxHealth
            #set that the player has spawned
            self.PlayerSpawned = True
            #say that the player is not being killed by fire pit
            self.DeathByPit = False
            #stop the grapple if player was grappling when they died
            self.Owner.MasterPlayerContr.StopGrapple()
            #reset player velocity if player had directional velocity when the died
            self.Owner.RigidBody.Velocity = VectorMath.Vec3(0,0,0)
            
#---------------------------------------------------------------------------------------------------------------------
            #Based on what the random number is it will do one of these
            #Procedure is the same for all 34 phrases
            #refer to Phrase 1 for full explanation of procedure
            #Phrase code ends Line 478
            
            #Phrase 1
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
                    
            #Phrase 2
            elif(randPhrase == 2):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase2", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase2")
                self.Phrase = True
          
            #Phrase 3
            elif(randPhrase == 3):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase3", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase3")
                self.Phrase = True

            #Phrase 4
            elif(randPhrase == 4):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase4", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase4")
                self.Phrase = True
          
            #Phrase 5
            elif(randPhrase == 5):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase5", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase5")
                self.Phrase = True
                
            #Phrase 6
            elif(randPhrase == 6):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase6", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase6")
                self.Phrase = True
          
            #Phrase 7
            elif(randPhrase == 7):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase7", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase7")
                self.Phrase = True
            
            #Phrase 8
            elif(randPhrase == 8):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase8", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase8")
                self.Phrase = True
          
            #Phrase 9
            elif(randPhrase == 9):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase9", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase9")
                self.Phrase = True
                
            #Phase 10
            elif(randPhrase == 10):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase10", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase10")
                self.Phrase = True
          
            #Phrase 11
            elif(randPhrase == 11):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase11", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase11")
                self.Phrase = True

            #Phrase 12
            elif(randPhrase == 12):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase12", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase12")
                self.Phrase = True
          
            #Phrase 13
            elif(randPhrase == 13):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase13", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase13")
                self.Phrase = True
                
            #Phrase 14
            elif(randPhrase == 14):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase14", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase14")
                self.Phrase = True
          
            #Phrase 15
            elif(randPhrase == 15):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase15", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase15")
                self.Phrase = True

            #Phrase 16
            elif(randPhrase == 16):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase16", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase16")
                self.Phrase = True
          
            #Phrase 17
            elif(randPhrase == 17):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase17", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase17")
                self.Phrase = True
                  
            #Phrase 18
            elif(randPhrase == 18):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase18", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase18")
                self.Phrase = True
          
            #Phrase 19
            elif(randPhrase == 19):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase19", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase19")
                self.Phrase = True

            #Phrase 20
            elif(randPhrase == 20):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase20", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase20")
                self.Phrase = True
          
            #Phrase 21
            elif(randPhrase == 21):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase21", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase21")
                self.Phrase = True
                
            #Phrase 22
            elif(randPhrase == 22):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase22", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase22")
                self.Phrase = True
          
            #Phrase 23
            elif(randPhrase == 23):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase23", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase23")
                self.Phrase = True

            #Phrase 24
            elif(randPhrase == 24):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase24", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase24")
                self.Phrase = True
          
            #Phrase 25
            elif(randPhrase == 25):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase25", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase25")
                self.Phrase = True
                
            #Phrase 26
            elif(randPhrase == 26):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase26", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase26")
                self.Phrase = True
          
            #Phrase 27
            elif(randPhrase == 27):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase27", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase27")
                self.Phrase = True

            #Phrase 28
            elif(randPhrase == 28):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase28", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase28")
                self.Phrase = True
          
            #Phrase 29
            elif(randPhrase == 29):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase29", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase29")
                self.Phrase = True
                
            #Phrase 30
            elif(randPhrase == 30):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase30", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase30")
                self.Phrase = True
          
            #Phrase 31
            elif(randPhrase == 31):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase31", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase31")
                self.Phrase = True

            #Phrase 32
            elif(randPhrase == 32):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase32", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase32")
                self.Phrase = True
          
            #Phrase 33
            elif(randPhrase == 33):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase33", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase33")
                self.Phrase = True
                  
            #Phrase 34
            elif(randPhrase == 34):
                if(self.Phrase):
                    self.phrase.Destroy()
                    self.count = self.maxcount
                self.Space.CreateAtPosition("Phrase34", VectorMath.Vec3(self.Owner.Transform.Translation.x, self.Owner.Transform.Translation.y + 3, 1))
                self.phrase = self.Space.FindObjectByName("Phrase34")
                self.Phrase = True
                
        #If there is a phrase on the screen
        if(self.Phrase):
            #checks current timer count
            if(self.count <= 2):
                #counts down
                self.count -= UpdateEvent.Dt
            #if timer count is less than zero
            if(self.count < 0):
                #reset timer
                self.count = self.maxcount
                #destroy the phrase on the screen
                self.phrase.Destroy()
                #set that there is no phrase on the screen
                self.Phrase = False
#---------------------------------------------------------------------------------------------------------------------
            
        #if you are't dead you're fine
        elif(self.PlayerSpawned == True):
            pass
            
        #regen procedure
        if(self.RegenStart > self.RegenCounter):
            #will increase health back to max health
            if(self.Health < self.MaxHealth):
                self.Health += 1 ** UpdateEvent.Dt
            
            #once health is back to max health it will reset regen variables
            else:
                self.RegenStart = 0
                self.Health = self.MaxHealth
        
        #logic for creating sound cues for different levels of health
        if(UpdateEvent.CurrentTime > self.nextPing):
            self.nextPing = UpdateEvent.CurrentTime + self.pingDelay
            if(self.hurt == True):
                self.Space.SoundSpace.PlayCue("hurtlittle")
            if(self.hurtmore == True):
                self.Space.SoundSpace.PlayCue("hurtmedium")
            if(self.hurtmost == True):
                self.Space.SoundSpace.PlayCue("hurtmax")

        #creating a variable for the HUD
        hudSpace = Zero.Game.FindSpaceByName("HUDSpace")
        #if there is no HUD do nothing (orignally for tutorials)
        if(not hudSpace):
            pass
        #otherwise create a varaible for the death count object in HUD
        else:
            deathObject = hudSpace.FindObjectByName("DCounter")
            #if the object exists
            if(deathObject):
                #set the value to the number of deaths
                deathObject.SpriteText.Text = str(self.totalDeath)
                
                
    def OnCollisionStart(self, CollisionEvent):
    #Set up for enemy collisions and fire pit collisions
    
        #"Bat" type enemy hurts you
        if(CollisionEvent.OtherObject.Name == "Bat"):
            self.Health -= 50.0 #Subtract 50 health points
            self.RegenStart = 0 #Restart regen procedure
            
            #play hit sound effect
            self.Space.SoundSpace.PlayCue("hit")

        #"Goblin" type enemy hurts you
        if(CollisionEvent.OtherObject.Name == "Goblin"):
            self.Health -= 50.0 #Subtract 50 health points
            self.RegenStart = 0 #Restart regen procedure
            
            #play hit sound effect
            self.Space.SoundSpace.PlayCue("hit")

        #If you are killed by a fire pit
        if(CollisionEvent.OtherObject.Name == "Pit"):
            #set that the fire pit did kill you
            self.DeathByPit = True
            #make a fizzle effect
            self.Space.CreateAtPosition("Fizzle", self.Owner.Transform.Translation)
            #sets health so low to initialize respawn sequence
            self.Health = -38
           
Zero.RegisterComponent("Health", Health)