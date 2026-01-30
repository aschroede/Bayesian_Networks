"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk, Andrew Schroeder

Class for the implementation of the variable elimination algorithm.

"""
from factor import Factor
from read_bayesnet import BayesNet


class MAP():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def run(self, map_vars:list, observed: dict, elim_heuristic=None):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            map_vars:       The map variables to be queried
            observed:       A dictionary of the observed variables {variable: value}
            elim_heuristic: String to specify which elimination order heuristic to use.
                            That that the tests in test_map.py pass none so you should implement a default elim order
                            heuristic if none is provided.

        Output: A dictionary representing the most probable assignment to the map variables {variable: value}

        """

        #TODO Implement this method
        pass