"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from variable_elim import VariableElimination
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
            ve = VariableElimination(net)
            query = 'Alarm'
            evidence = {'Burglary': 'True'}
        elif example_selection == 2:
            net = BayesNet('Networks/alarm.bif')
            ve = VariableElimination(net)
            query = 'Tampering'
            evidence = {'Smoke': '1', 'Report': '1'}
        else:
            break

        # Select Heuristic
        heuristic_selection = int(input(f"Select elimination order heuristic:\n"
                                        f"1) {least_incoming}\n"
                                        f"2) {fewest_factors}\n"))

        # Get elimination order
        if heuristic_selection == 1:
            elim_order = min_parents(net)
            elim_type = least_incoming
        else:
            elim_order = min_factors(net)
            elim_type = fewest_factors

        # Remove query and evidence nodes from elim order
        elim_order.remove(query)
        for var in evidence.keys():
            elim_order.remove(var)

        # Log Information
        logger.info("------- NEW VE RUN STARTED -------")
        logger.info("Date: " + str(datetime.now()))
        logger.info("Elimination order heuristic used: " + elim_type)
        logger.info("Elimination Order: " + str(elim_order))

        # Run VE
        ve.run(query, evidence, elim_order)
        print("\nVerbose log output saved to " + logger.handlers[0].baseFilename)


if __name__ == '__main__':
    main()
