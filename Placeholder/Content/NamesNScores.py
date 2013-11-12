import Zero
import Events
import Property
import VectorMath

class NamesNScores:
    def __init__(self, nameInc, scoreInc):
        self.name = nameInc
        self.score = scoreInc
        
        
    def ScoreCheck(self, checkedScores):
        if(checkedScores.score >= self.score):
            return True
        return False
        
        