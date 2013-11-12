import Zero
import Events
import Property
import VectorMath

class ScoreOff:
    def Initialize(self, initializer):
        Zero.Game.Score.tutorial = True

Zero.RegisterComponent("ScoreOff", ScoreOff)