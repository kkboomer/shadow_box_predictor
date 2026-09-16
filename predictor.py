import random
class Predictor:
    def __init__(self):
        self.history = []
        self.unigrams = {}
        self.bigrams = {}
        self.trigrams = {}
        self.possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    def update_history(self, move):
       self.unigrams[move] = self.unigrams.get(move, 0) + 1
       if len(self.history) >= 1:
            # use bigram model for prediction
            last_move = self.history[-1]
        
        
       self.history.append(move)



