"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk, Andrew Schroeder

Class for the implementation of the variable elimination algorithm.

"""
from factor import Factor
from read_bayesnet import BayesNet
from logger import logger


class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def run(self, query, observed: dict, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable

        """
        # Somehow get data into factors that support reduction, maximisation, and marginalization

        logger.info("Query Variables: " + query)
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

            # Marginalize out the variable to be eliminated
            result.marginalize(var_to_eliminate)
            logger.debug("Sum out " + var_to_eliminate)
            self.log_factor(result)

            # Remove used factors and replace with new one in list of factors
            for factor in to_multiply:
                factors.remove(factor)
            factors.append(result)
            logger.debug("New List of Factors: ")
            self.log_factors(factors)

        logger.debug("Elimination step complete. Multiply the following remaining factors together.")
        if len(factors) > 1:
            self.log_factors(factors)
        else:
            self.log_factor(factors[0])

        # Multiply remaining factors
        result = factors[0]
        if len(factors) > 1:
            for factor in factors[1:]:
                result.multiply(factor, query)
        logger.debug("Final factor pre-normalization.")
        self.log_factor(result)

        # Need to normalize as well
        result.normalize()
        logger.info("Final factor post-normalization.")
        self.log_factor(result, info=True)

        return result

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
