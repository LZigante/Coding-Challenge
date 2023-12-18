# -*- coding: utf-8 -*-
"""
____________________TITLE____________________
The Chocolate Bar Problem: A Coding Challenge
_____________________________________________

Description: There are m chocolate bars of varying (integer) lengths and
n hungry children who want differing amounts of chocolate (again integer
amounts). The aim is to feed all of the children the correct amount whilst
making the fewest cuts to the chocolate bars.

This program breaks the problem up into the following stages:
1) Any chocolate bars of length that already match a hungry child's demand
    is given - this satisfies a demand without the need for a cut.
2) Child demands that may be met by summing multiple chocolate bars are met -
    this also satisfies a demand without requiring a cut.
3) Choose cuts such that the 2 resulting bars each satisfy a child's demand -
    this ensures cuts are done efficiently
4) Remaining demands are met by cutting a chocolate bar to match - this is
    the least cut-efficient step.

*Values for the chocolate bars and children demands should be entered
at the start of the main function.

Lewis Zigante 18/12/2023
"""

from collections import Counter
import sys
import numpy as np


def insufficient_chocolate(demands, bars):
    """
    Function called when there is insufficient chocolate to meet the
    demands of the children. Prints how much more chocolate would be required,
    before waiting for any input and subsequently exiting the program.

    """
    missing_squares = np.sum(demands) - np.sum(bars)
    input('Insufficient chocolate to meet children demands. '
          f'Require at least {missing_squares} more chocolate. '
              'Press Enter to exit.')
    sys.exit() # Exits the program


def remove_common_elements(bars, demands):
    """
Takes the bars and demands lists, removes each instance of shared elements,
sorts the lists, and returns them.

    """
    count_bars = Counter(bars)
    count_demands = Counter(demands)
    bars = sorted((count_bars - count_demands).elements())
    demands = sorted((count_demands - count_bars).elements())

    return bars, demands


def try_bar_sums(bars, demands):
    """
Attempts to meet demands by summing existing bars.
For each demand, the smallest bar is subtracted from it, and the resulting
value is looked up in the bars counter container. If it exists, the bars
contributing to the sum are removed from the bars list and counter. If not,
the next bar is subtracted, and the result checked once more. This repeats
until the total drops below zero, or is found in the counter.

w and x are iteration counters for the demands and bars lists, respectively.
They provide access to each element.

    """
    w = 0
    demand_index_list = [] # Keeps track of which demands to remove
    count_bars = Counter(bars)
    bars = list(bars)
    while w < len(demands):
        x = 0
        count_bars_copy = count_bars.copy()
        bars_copy = bars.copy()
        prev = demands[w]
        while x < len(bars):
            bar = bars[x]
            curr = prev - bar
            bars_copy.pop(0)
            count_bars_copy[bar] -= 1

            if curr < 0:
                w += 1
                break

            if curr in count_bars_copy and count_bars_copy[curr] > 0:
                bars_copy.remove(curr)
                bars = bars_copy
                count_bars_copy[curr] -= 1
                count_bars = count_bars_copy
                demand_index_list.append(w)
                w += 1
                break

            prev = curr
            x += 1

    demands = np.array(demands)
    if len(demand_index_list) == 0:
        return bars, demands

    return bars, np.delete(demands, demand_index_list)


def do_remaining_cuts(demands, cuts):
    """
Makes cuts to meet the remaining demands. Each demand corresponds to one cut,
until there are two demands left, which may always be satisfied with one cut.

    """
    num_demands = len(demands)
    if num_demands > 1:
        return cuts + num_demands - 1
    if num_demands == 0:
        return cuts

    return cuts + 1


def try_efficient_cuts(bars, demands, cuts):
    """
Makes cuts such that the two resulting bars each satisfy a demand.

left and right are the two pointers of a sliding window that searches for
the target value in the demands list
w is an iteration counter, allowing access to each bar.


    """
    w = 0
    bar_index = [] # keeps track of the indices to remove from bars
    demands = list(demands)
    while w < len(bars):
        left = 0
        right = len(demands) - 1

        if right <= 0:
            break

        target = bars[w]

        if demands[0] + demands[1] > target: # skips to next bar if smaller
            w += 1                           # than two smallest demands
            continue

        while left <= right:
            curr = demands[left] + demands[right] # initialise dynamic window
                                                  # at either end of demands
            if left == right: # No two demands summing to the bar were found
                w += 1
                break

            if curr > target:
                right -= 1

            elif curr < target:
                left += 1

            else:
                demands.pop(left) # two demands equal target bar
                demands.pop(right - 1)
                cuts += 1
                bar_index.append(w)
                # bars.pop(w)
                break

    bars = np.array(bars)
    if len(bar_index) == 0:
        return bars, demands, cuts
    return np.delete(bars, bar_index), demands, cuts

def trivial_end_condition(bars, demands, cuts):
    """
Called after each step to check if the trivial cases have been reached for
the demands and bars lists.

    """
    if len(demands) == 0:
        return [True, cuts]
    if len(demands) == 1:
        return [True, cuts + 1]
    if len(bars) == 1:
        cuts += len(demands) - 1
        return [True, cuts]

    return [False, cuts]

def main():
    """
    The main function.
    Attempts to finds the minimum number of cuts to distribute the chocolate
    amongst the children.

    Returns cuts -> int

    """
    Cuts = 0
    # Enter the chocolate bars and children demands here
    chocolate_bars = [2, 5, 7]
    children_demands = [4, 3, 2, 1]
    # chocolate_bars = np.random.randint(1, 60, size = 100)
    # children_demands = np.random.randint(1, 40, size = 120)

# Handles the condition where there is insufficient chocolate to meet demands
    if sum(chocolate_bars) < sum(children_demands):
        insufficient_chocolate(children_demands, chocolate_bars)

# Checks if any chocolate bars already meet any demands. Removes them from
# each list and sorts the lists before returning them.
    chocolate_bars, children_demands = remove_common_elements(chocolate_bars,
                                                              children_demands)

    # end condition called after each stage to check trivial cases
    end_condition = trivial_end_condition(chocolate_bars, children_demands,
                                                                          Cuts)
    if end_condition[0]:
        Cuts = end_condition[1]
        return Cuts

# Tries to find demands that can be met by combining multiple bars
    chocolate_bars, children_demands = try_bar_sums(chocolate_bars,
                                                    children_demands)
    end_condition = trivial_end_condition(chocolate_bars, children_demands,
                                                                          Cuts)
    if end_condition[0]:
        Cuts = end_condition[1]
        return Cuts

# Looks to make optimal cuts such that 2 demands are satisfied with one cut
    chocolate_bars, children_demands, Cuts = try_efficient_cuts(chocolate_bars,
                                                        children_demands, Cuts)

    end_condition = trivial_end_condition(chocolate_bars, children_demands,
                                                                          Cuts)
    if end_condition[0]:
        Cuts = end_condition[1]
        return Cuts

# Makes cuts to meet the remaining demands
    Cuts = do_remaining_cuts(children_demands, Cuts)

    return Cuts


if __name__ == '__main__':
    Cuts = main()
    print(f"Cuts needed to share chocolate: {Cuts}")
