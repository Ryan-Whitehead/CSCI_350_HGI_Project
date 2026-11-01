from player import Player
from itertools import permutations

class HGI_B3(Player):
  """Baseline 3: learn color counts with single-color guesses, then guess
  consistent codes."""

  def __init__(self):
    self.player_name = "HGI_B3"
    self._reset_round()

  def _reset_round(self):
     self.history = []
     self.color_counts = {}
     self.last_guess = None
     self.candidates = []
     

  def make_guess(self, board_length, colors, scsa_name, last_response):
    exact, other, guess_number = last_response

    if guess_number == 0: # first guess of a new round
      self._reset_round()
    else:
      self.history.append((self.last_guess, exact, other))
      if guess_number <= len(colors) -1:
        self.color_counts[colors[guess_number -1]] = exact

    guess = self._next_guess(board_length, colors)   
    self.last_guess = guess
    return guess   

  def _next_guess(self, board_length, colors):
    # phase 1: next single-color guess
    n = len(self.history)
    if n < len(colors) -1:
      return colors[n] * board_length

    #phase 2: the last color's count is whatever is left over
    if n == len(colors) - 1:
      self.color_counts[colors[-1]] = board_length - sum(self.color_counts.values())
      self._generate_candidates()

    if self.candidates:
      return self.candidates.pop()
      
    return colors[0] * board_length  

  def _generate_candidates(self):
    pool = []
    for color, count in self.color_counts.items():
      pool += [color] * count
    self.candidates = [''.join(t) for t in set(permutations(pool))]

