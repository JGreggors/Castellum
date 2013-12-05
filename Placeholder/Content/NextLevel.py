########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class NextLevel:
#Logic for loading a level when a player reaches the end of a level

    #Storing the current level number (Ex. Level 5 = 5)
    #stored for score purposes
    LevelNumber = Property.Int(0)
    
    def Initialize(self, initializer):
        
        #Creating a collision event
        Zero.Connect(self.Owner, Events.CollisionStarted, self.OnCollisionStart)
        #setting whether the end of the level is reached
        self.EndGame = False
        
    def OnCollisionStart(self, CollisionEvent):
        
        #setting a variable for a collision object
        otherObject = CollisionEvent.OtherObject
        
        #if the end of level door object collides with the player
        if(otherObject.Name == "Player"):
            #load the next level in the level table
            Zero.Game.Score.LevelNumber = self.LevelNumber
            #set that the end of the level has been reached
            self.EndGame = True
        
Zero.RegisterComponent("NextLevel", NextLevel)