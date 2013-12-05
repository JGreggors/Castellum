########################################################################
##All content (c) 2013 DigiPen (USA) Corporation, all rights reserved.##
########################################################################

import Zero
import Events
import Property
import VectorMath

class ScoreOn:
#Logic to turn  Score on for that level

    def Initialize(self, initializer):
        Zero.Game.Score.tutorial = False

Zero.RegisterComponent("ScoreOn", ScoreOn)