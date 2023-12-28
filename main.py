import argparse
from strategies.strategies import all_strategies
from yahtzee.yahtzee import Yahtzee
import matplotlib.pyplot as plt
import numpy as np

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

def main():
    strategy = None

    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-r', '--runs', type=int, default=1)      # option that takes a value
    parser.add_argument('-q', '--quiet',
                        action='store_true', default=False)  # on/off flag
    parser.add_argument('-i', '--interactive',
                    action='store_true', default=False)  # on/off flag
    parser.add_argument('-p', '--show-plot', dest='show_plot',
                    action='store_true', default=False)  # on/off flag
    parser.add_argument('-s', '--strategy',
                        choices=all_strategies.keys())  # on/off flag
    
    args = parser.parse_args()

    if args.runs > 1:
        quiet_mode = True

    scores_list = []
    for _ in range(args.runs):
        strategy = all_strategies[args.strategy]()
        game = Yahtzee(strategy, args.interactive)
        score = game.run()
        scores_list.append(score)
        if not quiet_mode:
            input("press any key to continue")
    if args.show_plot:
        show_plot(scores_list)

main()