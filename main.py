import argparse
from strategies.strategies import all_strategies
from yahtzee.yahtzee import Yahtzee
import matplotlib.pyplot as plt
import numpy as np
import curses

def show_plot(scores_list):
    # Calculate the median
    median_score = np.median(scores_list)

    # Create the histogram
    plt.hist(scores_list, bins=100, edgecolor='black', alpha=0.7)

    # Add a red vertical line at the median
    plt.axvline(median_score, color='red', linestyle='dashed', linewidth=2)

    # Annotate the median value
    plt.text(median_score, plt.ylim()[1]*0.9, f'Median: {median_score}', color = 'red')

    # Adding titles and labels
    plt.title('Histogram of Scores with Median')
    plt.xlabel('Scores')
    plt.ylabel('Frequency')

    # Display the plot
    plt.show()
    print("average score", sum(scores_list) / len(scores_list))

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlighted: Black text on white bg
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Non-highlighted: White text
    strategy = None

    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-r', '--runs', type=int, default=1)
    parser.add_argument('-q', '--quiet',
                        action='store_true', default=False)
    parser.add_argument('-i', '--interactive',
                    action='store_true', default=False)
    parser.add_argument('-p', '--show-plot', dest='show_plot',
                    action='store_true', default=False)
    parser.add_argument('-s', '--strategy',
                        choices=all_strategies.keys())
    
    args = parser.parse_args()

    quiet_mode = args.quiet
    if args.runs > 1:
        quiet_mode = True

    scores_list = []
    for _ in range(args.runs):
        strategy = all_strategies[args.strategy]()
        game = Yahtzee(strategy, args.interactive, stdscr)
        score = game.run()
        scores_list.append(score)
        if not quiet_mode:
            print("Final score:", score)
    if args.show_plot:
        show_plot(scores_list)

if __name__ == "__main__":
    curses.wrapper(main)
