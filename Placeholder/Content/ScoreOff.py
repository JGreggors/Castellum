########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class ScoreOff:
#Logic to turn  Score off for that level

    def Initialize(self, initializer):
        Zero.Game.Score.tutorial = True

Zero.RegisterComponent("ScoreOff", ScoreOff)