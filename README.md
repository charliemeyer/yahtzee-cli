# Yahtzeeql - Yahtzee solver that's mostly SQL

## Setup

```
python3 -m venv yahtzee-venv
source yahtzee-venv/bin/activate
pip install -r requirements.txt
./test.sh
```

You should see outputs for each strategy, in ascending order by goodness

## Usage

```
python3 yahtzee.py --strategy <strategy> --runs <runs> [--interactive] [--show-plot]
```

Where `strategy` is one of:

- `random` - just keep the dice you're given, and pick a random category
- `random_greedy` - just keep the dice you're given, and pick the category that gives the highest score
- `all_yahtzee` - Do everything possible to get a Yahtzee every turn
- `prob` - Use probability tables to maximize the fraction of points you earn
- `prob_with_difficulty` - Use probability tables to maximize the fraction of points you earn, considering the difficulty of each category

`--runs` is the number of games to simulate

`--interactive` will show you the dice and ask you to pick a category for each turn

`--show-plot` will show you a plot of the score distribution

## Probabilty tables

`build_prob_db.py` generates a sqlite database with a few tables:

- `all_rolls` - All rolls of 5 dice, with dice sorted in ascending order
- `roll_transitions` - The probability of transitioning from one roll to another, while keeping some subset of the first roll
- `level0` - For each roll, its score in each category, reprersented as a fraction of the maximum possible score in that category, and the raw score
- `level1` - For each roll, the expected value of each roll/keep/strategy combination, based on the sum of the expected values of each possible next roll from the level1 table

## Results

- `random` - 84.5
- `random_greedy` - 86.5
- `all_yahtzee` - 87.5
- `prob` - 88.5
- `prob_with_difficulty` - 89.5
