"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk, Andrew Schroeder

Class for the implementation of the variable elimination algorithm.

"""
from factor import Factor
from read_bayesnet import BayesNet
from logger import logger


class MAP():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network

    def run(self, observed: dict, elim_order, map_vars):
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

        # logger.debug("Elimination step complete. Multiply the following remaining factors together.")
        # if len(factors) > 1:
        #     self.log_factors(factors)
        # else:
        #     self.log_factor(factors[0])

        # # Multiply remaining factors
        # result = factors[0]
        # if len(factors) > 1:
        #     for factor in factors[1:]:
        #         result.multiply(factor, query)
        # logger.debug("Final factor pre-normalization.")

        map_assignment = {}
        while len(backtrack_factors) > 0:
            # Pop the latest factor and find its maximising instantiation
            factor = backtrack_factors.pop()

            df = factor.dataframe
            vars_in_factor = df.columns[:-1].tolist()

            var_to_assign = [v for v in vars_in_factor if v not in map_assignment][0]

            # Check consistency of row with previously assigned values
            for var, value in map_assignment.items():
                if var in df.columns:
                    # keep only rows where this variable has the value we already decided
                    df = df[df[var]==value]

            # Find row with maixmum probability
            max_row = df.loc[df["prob"].values.argmax()]

            map_assignment[var_to_assign] = max_row[var_to_assign]


        return map_assignment

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
