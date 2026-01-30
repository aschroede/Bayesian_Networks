"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination
from map import MAP
from elim_order_heuristics import min_factors, min_parents
from logger import logger
from datetime import datetime
import time

least_incoming = "Least incoming arcs first"
fewest_factors = "Contained in fewest factors first"
earthquake_example = "Earthquake"
alarm_example1 = "Alarm 1"
alarm_example2 = "Alarm 2"
def main():


    while True:

        # Select example
        example_selection = int((input(f"\nSelect an example query:\n"
                                       f"1) {earthquake_example}\n"
                                       f"2) {alarm_example1}\n"
                                       f"3) {alarm_example2}\n"
                                       "4) Quit\n")))

        # Reset vars for each run since they are static
        BayesNet.values.clear()
        BayesNet.probabilities.clear()
        BayesNet.parents.clear()

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
                                        f"1) {least_incoming}\n"
                                        f"2) {fewest_factors}\n"))



        # Log Information
        logger.info("------- NEW MAP RUN STARTED -------")
        logger.info("Date: " + str(datetime.now()))
        logger.info("Elimination order heuristic used: " + elim_type)
        logger.info("Non-MAP Elimination Order: " + str(non_map_elim_order))
        logger.info("MAP Elimination Order: " + str(map_elim_order))

        # Run VE
        map_result = map.run(map_vars, evidence, combined_elim_order)
        print(f"Map Result: {map_result}")
        print("\nVerbose log output saved to " + logger.handlers[0].baseFilename)


if __name__ == '__main__':
    main()
