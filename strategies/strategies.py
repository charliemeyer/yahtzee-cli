from strategies.all_yahtzee_strategy import AllYahtzee
from strategies.random_greedy_strategy import RandomGreedy
from strategies.random_strategy import CompletelyRandom
from strategies.prob_strategy import ProbStrategy
from strategies.prob_with_difficulty_strategy import ProbWithDifficulty

all_strategies = {
    "all_yahtzee": AllYahtzee,
    "random_greedy": RandomGreedy,
    "random": CompletelyRandom,
    "prob": ProbStrategy,
    "prob_with_difficulty": ProbWithDifficulty,
}