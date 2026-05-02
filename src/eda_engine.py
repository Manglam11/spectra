import pandas as pd
import numpy as np

class EDAEngine:
    """
    Compute full statistical profile of a loaded DataFrame.
    Handles numeric and categorical columns separately.
    """

    def __init__(self, df:pd.DataFrame):
        """
        Store df and pre-separate numeric vs categorical cols

        """
        self.df = df.copy()
        self.df_numeric = self.df.select_dtypes(include="number")
        self.df_categorical = self.df.select_dtypes(include="object")


    def get_numeric_summary(self) -> pd.DataFrame:
        """
        Perform operations specific to numerical type of column.

        Returns:
            DataFrame:
                mean: mean of each column

                median: median of each column

                std: std of each column

                skewness: skewness of each column

                kurtosis: kurtosis of each column

                min_value: smallest numeric point in each column

                max_value: largest numeric point in each column

                missing_count: number of missing values

                missing_pct: percentage of missing values

        """
        results = {}

        for col in self.df_numeric:
            missing = self.df_numeric[col].isna().sum()
            results[col] = {
                "mean": self.df_numeric[col].mean(),
                "median": self.df_numeric[col].median(),
                "std": self.df_numeric[col].std(),
                "skewness": self.df_numeric[col].skew(),
                "kurtosis": self.df_numeric[col].kurt(),
                "min_value": self.df_numeric[col].min(),
                "max_value": self.df_numeric[col].max(),
                "missing_count": missing,
                "missing_pct": round((missing/len(self.df_numeric[col])) * 100, 2)
            }

        return pd.DataFrame(results).T

    def get_categorical_summary(self) -> pd.DataFrame:
        """
        Perform operations specific to string type of column.

        Returns:
            DataFrame:
                unique_count: how many distinct values

                top_value: most frequent value (mode)

                top_freq: how many times the top value appears

                missing_count: number of nulls

                missing_pct: percentage of missing values

        """
        results = {}

        for col in self.df_categorical:
            missing = self.df_categorical[col].isna().sum()
            results[col] = {
                "unique_count": self.df_categorical[col].nunique(),
                "top_value": self.df_categorical[col].mode()[0] if not self.df_categorical[col].mode().empty else None,
                "top_freq": self.df_categorical[col].value_counts().iloc[0] if not self.df_categorical[col].value_counts().empty else None,
                "missing_count": missing,
                "missing_pct": round((missing/len(self.df_categorical[col])) * 100, 2)
            }

        return pd.DataFrame(results).T

