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
            if last_move not in self.bigrams:
                self.bigrams[last_move] = {}
            self.bigrams[last_move][move] = self.bigrams[last_move].get(move, 0) + 1
        if len(self.history) >= 2:
            last_two_moves = tuple(self.history[-2:])
            if last_two_moves not in self.trigrams:
                self.trigrams[last_two_moves] = {}
            self.trigrams[last_two_moves][move] = self.trigrams[last_two_moves].get(move, 0) + 1
        self.history.append(move)
    
    def predict_next_move(self):
        counts = {}
        model = "random"
        
        if not self.history:
            return random.choice(self.possible_moves), 0.25, model
        # we go down in cascading order from trigrams down to unigrams
        if len(self.history) >= 2:
            last_two_moves = tuple(self.history[-2:])
            if last_two_moves in self.trigrams:
                counts = self.trigrams[last_two_moves]
                model = "trigram"
            elif not counts and len(self.history) >= 1:
                last_move = self.history[-1]
                if last_move in self.bigrams:
                    counts = self.bigrams[last_move]
                    model = "bigram"
            elif not counts and len(self.unigrams) >= 0:
                counts = self.unigrams
                model = "unigram"
            # we do lapalce smoothing to prevent zero probabilities
            V, N = 4, sum(counts.values())
            smoothed_prob = {}
            for move in self.possible_moves:
                smoothed_prob[move] = (counts.get(move, 0) + 1) / (N + V)
            max_prob = max(smoothed_prob.values())
            best_moves = [move for move, prob in smoothed_prob.items() if prob == max_prob]
            return random.choice(best_moves), max_prob, model


