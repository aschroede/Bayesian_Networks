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
alarm_example = "Alarm"
def main():


    while True:

        # Select example
        example_selection = int((input(f"\nSelect an example query:\n"
                                       f"1) {earthquake_example}\n"
                                       f"2) {alarm_example}\n"
                                       "3) Quit\n")))

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
        else:
            break

        map = MAP(net)

        # Select Heuristic
        heuristic_selection = int(input(f"Select elimination order heuristic:\n"
                                        f"1) {least_incoming}\n"
                                        f"2) {fewest_factors}\n"))


        # Need to get list of map vars and list of non map vars and then get separate elim orders for them
        non_map_vars = net.nodes.copy()
        # remove map vars
        for var in map_vars:
            non_map_vars.remove(var)
        # remove evidence vars
        for var in evidence.keys():
            non_map_vars.remove(var)


        # Get elimination order
        if heuristic_selection == 1:

            elim_order = min_parents(net)

            non_map_elim_order = [var for var in elim_order if var in non_map_vars]
            map_elim_order = [var for var in elim_order if var in map_vars]

            elim_type = least_incoming
        else:
            elim_order = min_factors(net)

            non_map_elim_order = [var for var in elim_order if var in non_map_vars]
            map_elim_order = [var for var in elim_order if var in map_vars]

            elim_type = fewest_factors

        # Need to marginalise out non map variables first then maximise out map variables second
        combined_elim_order = non_map_elim_order+map_elim_order

        # Log Information
        logger.info("------- NEW MAP RUN STARTED -------")
        logger.info("Date: " + str(datetime.now()))
        logger.info("Elimination order heuristic used: " + elim_type)
        logger.info("Non-MAP Elimination Order: " + str(non_map_elim_order))
        logger.info("MAP Elimination ORder: " + str(map_elim_order))

        # Run VE
        map_result = map.run(evidence, combined_elim_order, map_vars)
        print(f"Map Result: {map_result}")
        print("\nVerbose log output saved to " + logger.handlers[0].baseFilename)


if __name__ == '__main__':
    main()
