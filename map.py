"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk, Andrew Schroeder

Class for the implementation of the variable elimination algorithm.

"""
from factor import Factor
from read_bayesnet import BayesNet
from logger import logger
from elim_order_heuristics import *


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

        elim_order = self.get_map_elim_order(map_vars, observed, elim_heuristic)

        logger.info("Elimination Order: " + str(elim_order))
        logger.info("MAP Variables: "+ str(map_vars))
        logger.info("Observed Variables: " + str(observed))

        assert isinstance(self.network, BayesNet)

        # Convert cpts to factors
        factors = self.get_factors_from_cpts()

        logger.debug("Original Factors: ")
        self.log_factors(factors)

        # Clamp evidence in the factors
        to_delete = []
        for variable, value in observed.items():
            for factor in factors:
                if variable in factor.get_vars():
                    factor.reduce(variable, value)
                    # Check if factor is trivial
                    if factor.get_data_frame().columns[:].tolist() == ["prob"]:
                        to_delete.append(factor)

        # If factor is trivial after reduction, delete it from list
        for factor in to_delete:
            factors.remove(factor)

        logger.debug("Factors with evidence applied: ")
        self.log_factors(factors)

        backtrack_factors = []

        # Use provided elimination order
        for var_to_eliminate in elim_order:

            logger.debug("Eliminate variable: " + var_to_eliminate)

            # Collect all factors to be multiplied
            to_multiply = [factor for factor in factors if any(var == var_to_eliminate for var in factor.get_vars())]
            logger.debug("Factors to multiply containing variable: " + var_to_eliminate)
            self.log_factors(to_multiply)

            # Multiply together
            result = to_multiply[0]
            for factor in to_multiply[1:]:
                result.multiply(factor, var_to_eliminate)
            logger.debug("Result of multiplication: ")
            self.log_factor(result)

            # Only makes sense to marginalize and maximise if the factor has
            # at least two variables. TODO: This is not the correct way...
            #if len(result.dataframe.columns) > 2:

            # If non-map variable then marginalize out
            if var_to_eliminate not in map_vars:
                # Marginalize out the variable to be eliminated
                result.marginalize(var_to_eliminate)
                logger.debug("Sum out " + var_to_eliminate)
                self.log_factor(result)

            # Otherwise this is a map variable to be maximised out
            else:
                # Store this factor in a stack for use in backtracking to find map instantiation later
                logger.debug(f"Storing factor for backtracking to find value of {var_to_eliminate}")
                self.log_factor(result)
                backtrack_factors.append(result.copy())

                # Only maximise if there are at least two variables in the factor because otherwise
                # the factor is empty
                if (len(result.dataframe.columns) -1 >= 2):
                    result.maximize(var_to_eliminate)
                    logger.debug("Maximise out " + var_to_eliminate)
                    self.log_factor(result)

            # Remove used factors and replace with new one in list of factors
            for factor in to_multiply:
                factors.remove(factor)
            factors.append(result)
            logger.debug("New List of Factors: ")
            self.log_factors(factors)

        logger.debug("Finished marginalizing/maximising variables. Start backtracking to find variable instantiations.")
        map_assignment = self.get_map_instantiation(backtrack_factors)

        return map_assignment

    def get_map_instantiation(self, backtrack_factors):
        map_assignment = {}
        while len(backtrack_factors) > 0:
            # Pop the latest factor and find its maximising instantiation
            factor = backtrack_factors.pop()
            logger.debug("Popped this factor from the backtracking stack:")
            self.log_factor(factor)

            df = factor.dataframe
            vars_in_factor = df.columns[:-1].tolist()

            var_to_assign = [v for v in vars_in_factor if v not in map_assignment][0]
            logger.debug(f"Finding MAP instantiation for {var_to_assign}")

            # Check consistency of row with previously assigned values
            for var, value in map_assignment.items():
                if var in df.columns:
                    # keep only rows where this variable has the value we already decided
                    df = df[df[var]==value]

            # Find row with maixmum probability
            max_row = df.loc[df["prob"].idxmax()]

            map_assignment[var_to_assign] = max_row[var_to_assign]
            logger.debug(f"MAP assignment for variable {var_to_assign} is {max_row[var_to_assign]}")

        logger.debug("Final Map Instantiation:")

        for key, value in map_assignment.items():
            logger.debug(f"{key}->{value}")
        return map_assignment

    def get_map_elim_order(self, map_vars, observed, elim_order):


        if elim_order == "min_parents":
            order = min_parents(self.network)
        else:
            order = min_factors(self.network)


        non_map_vars = self.network.nodes.copy()
        # remove map vars
        for var in map_vars:
            non_map_vars.remove(var)
        # remove evidence vars
        for var in observed.keys():
            non_map_vars.remove(var)

        non_map_var_order = [var for var in order if var in non_map_vars]
        map_var_order = [var for var in order if var in map_vars]
        elim_order = non_map_var_order + map_var_order
        return elim_order

    # Logging functions
    def log_factors(self, factors):
        for factor in factors:
            logger.debug('\t' + factor.get_data_frame().to_string().replace('\n', '\n\t'))

    def log_factor(self, factor, info=False):
        if info:
            logger.info('\t' + factor.get_data_frame().to_string().replace('\n', '\n\t'))
        else:
            logger.debug('\t' + factor.get_data_frame().to_string().replace('\n', '\n\t'))

    def get_factors_from_cpts(self):
        factors = []
        for name, cpt in self.network.probabilities.items():
            factors.append(Factor(cpt))

        return factors
