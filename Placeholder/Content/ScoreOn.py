import Zero
import Events
import Property
import VectorMath

class ScoreOn:
    def Initialize(self, initializer):
        Zero.Game.Score.tutorial = False

Zero.RegisterComponent("ScoreOn", ScoreOn)