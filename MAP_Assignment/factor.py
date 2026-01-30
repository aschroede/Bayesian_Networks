import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


class Factor:

    def __init__(self, cpt: pd.DataFrame):
        self.dataframe = cpt
        assert isinstance(self.dataframe, pd.DataFrame)

    def reduce(self, variable, value):
        """
        Reduces this factor by applying evidence to it. Evidence variable is removed from dataframe
        Args:
            variable: variable to apply evidence to
            value: evidence to apply
        """

        # TODO: Implement this method
        pass


    def maximize(self, variable):
        """
        Maximises out a variable from the factor. Used for MAP operation.

        :param self: Description
        :param variable: Variable to maximise out of the factor.
        """

        # TODO Implement this method
        pass


    def marginalize(self, variable):
        """
        Sums-out a variable from this factor
        Args:
            variable: variable to sum out
        """

        # TODO Implement this method
        pass

    def multiply(self, factor2: "Factor", variable):
        """
        Multiplies this factor with another provided factor, merging the two factors on a common variable
        Args:
            factor2: factor to multiply this with
            variable: variable to merge the two factors on
        """

        # TODO Implement this method
        pass

    def normalize(self):
        """
        Normalizes this factor such that the probability distribution adds to 1
        """

        # TODO Implement this method
        pass


    def get_data_frame(self):
        return self.dataframe

    def get_vars(self):
        return self.dataframe.columns[:].tolist()

    def __str__(self) -> str:
        return str(self.get_vars())

    def copy(self):
        return Factor(self.dataframe.copy(deep=True))