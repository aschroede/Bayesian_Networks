"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from map import MAP
from datetime import datetime
import time

least_incoming = "Least incoming arcs first"
fewest_factors = "Contained in fewest factors first"
earthquake_example = "Earthquake"
alarm_example1 = "Alarm 1"
alarm_example2 = "Alarm 2"
def main():


    while True:

        # Reset vars for each run since they are static
        BayesNet.values.clear()
        BayesNet.probabilities.clear()
        BayesNet.parents.clear()

        # Select example
        example_selection = int((input(f"\nSelect an example query:\n"
                                       f"1) {earthquake_example}\n"
                                       f"2) {alarm_example1}\n"
                                       f"3) {alarm_example2}\n"
                                       "4) Quit\n")))

        # Example map queries
        if example_selection == 1:
            net = BayesNet('Networks/earthquake.bif')
            map_vars = ['Alarm']
            evidence = {'Burglary': 'True'}
        elif example_selection == 2:
            net = BayesNet('Networks/alarm.bif')
            map_vars = ['Tampering']
            evidence = {'Smoke': '1', 'Report': '1'}
        elif example_selection == 3:
            net = BayesNet('Networks/alarm.bif')
            map_vars = ['Tampering', 'Report']
            evidence = {'Smoke': '1'}

        else:
            break

        map = MAP(net)

        # Select Heuristic
        heuristic_selection = int(input(f"Select elimination order heuristic:\n"
                                        f"1) Mininum Parents\n"
                                        f"2) Minimum Factors\n"))

        if heuristic_selection == 1:
            elim_order = "min_parents"
        else:
            elim_order = "min_factors"


        # Run VE
        map_result = map.run(map_vars, evidence, elim_order)
        print(f"Map Result: {map_result}")


if __name__ == '__main__':
    main()
