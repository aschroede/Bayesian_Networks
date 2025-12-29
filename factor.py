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
        # Reduce table
        self.dataframe = self.dataframe[self.dataframe[variable] == value]

        # Remove variable that has been reduced
        self.dataframe.drop(variable, axis=1, inplace=True)

    def marginalize(self, variable):
        """
        Sums-out a variable from this factor
        Args:
            variable: variable to sum out
        """
        # Extract all variable columns (don't select last column which is probability column)
        all_columns = self.dataframe.columns[:-1]

        # Get all columns except for the column to be marginalized out
        columns_to_keep = [col for col in all_columns if col != variable]

        # Sum out variable by first grouping by the columns to keep and summing up each group
        # Calling reset_index() is necessary to prevent index out of range exception
        new_factor = self.dataframe.groupby(columns_to_keep).sum().reset_index()

        # Remove column for variable that has been summed out
        new_factor.drop(variable, axis=1, inplace=True)

        self.dataframe = new_factor

    def multiply(self, factor2: "Factor", variable):
        """
        Multiplies this factor with another provided factor, merging on the two factors on a common variable
        Args:
            factor2: factor to multiply this with
            variable: variable to merge the two factors on
        """
        # Get both dataframes from the associated factors
        f1_df = self.get_data_frame()
        f2_df = factor2.get_data_frame()

        # Get list of all column names, except "prob" columns
        all_columns = f1_df.columns[:-1].tolist() + f2_df.columns[:-1].tolist()
        # Use set to remove duplicate column names
        all_columns = list(set(all_columns))
        # Add a single "prob" column
        all_columns = all_columns + ["prob"]

        # Merge both dataframes on the common variable. Where duplicates exists add _1 and _2 suffixes
        # Only prob should have duplicates
        new_df = pd.merge(f1_df, f2_df, on=variable, suffixes=("_1", "_2"))

        # Make a new column in the table with the probabilities of individual dataframes multiplied together
        new_df["prob"] = new_df["prob_1"] * new_df["prob_2"]

        # Extract just the columns with the union of the variables in both sets and the multiplied probability
        new_df = new_df[all_columns]

        self.dataframe = new_df

    def normalize(self):
        """
        Normalizes this factor such that the probability distribution adds to 1
        """
        self.dataframe["prob"] = self.dataframe["prob"] / (self.dataframe["prob"].sum())

    def get_data_frame(self):
        return self.dataframe

    def get_vars(self):
        return self.dataframe.columns[:].tolist()

    def __str__(self) -> str:
        return str(self.get_vars())
