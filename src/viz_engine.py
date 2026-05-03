import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="darkgrid", palette="muted")


class VisualizationEngine:
    """
    Provides plot methods for numeric and categorical EDA visualizations.
    Uses Seaborn and Matplotlib under the hood.
    """

    def __init__(self, df:pd.DataFrame):
        """
        Stores the copy of dataframe.

        Args:
            df: data frame to be copied.
        """
        self.df = df.copy()

    def plot_histogram(self, column:str) -> None:
        """
        Plots the histogram of numeric type of column using seaborn library.

        Args:
            column: Numeric column you want to plot.
        """
        fig, ax = plt.subplots(figsize=(8,5))
        sns.histplot(
            data= self.df,
            x = column,
            ax = ax,
        )
        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(f"{column}")
        ax.set_ylabel("Frequency")

        plt.tight_layout()
        plt.show()


    def plot_bar(self, column:str) -> None:
        """
        Plots the bar chart of categorical type of column using seaborn library.

        Args:
            column: Categorical column you want to plot.
        """
        fig, ax = plt.subplots(figsize=(8,5))
        sns.countplot(
            data= self.df,
            x = column,
            ax = ax,
        )
        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(f"{column}")
        ax.set_ylabel("Count")

        plt.tight_layout()
        plt.show()

    def plot_scatter(self, col_x: str, col_y:str) -> None:
        """
        Plots the scatter plot of two numeric type of column using seaborn library.

        Args:
            col_x: First Numeric column (x-axis data).
            col_y: Second Numeric column (y-axis data).
        """
        fig, ax = plt.subplots(figsize=(8,5))
        sns.scatterplot(
            data= self.df,
            x = col_x,
            y = col_y,
            ax = ax,
        )
        ax.set_title(f"{col_x} vs {col_y}")
        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)

        plt.tight_layout()
        plt.show()

    def plot_violin(self, cat_col: str, num_col:str) -> None:
        """
        Plots the violin plot between category and numeric column using seaborn library.

        Args:
            cat_col: Categorical column (x-axis data).
            num_col: Numeric column (y-axis data).
        """
        fig, ax = plt.subplots(figsize=(8,5))
        sns.violinplot(
            data= self.df,
            x = cat_col,
            y = num_col,
            ax = ax,
        )
        ax.set_title(f"Distribution of {num_col} by {cat_col}")
        ax.set_xlabel(cat_col)
        ax.set_ylabel(num_col)

        plt.tight_layout()
        plt.show()

    def plot_correlation_heatmap(self) -> None:
        """
        Plots the correlation heatmap using seaborn library.

        """
        fig, ax = plt.subplots(figsize=(8,5))
        sns.heatmap(
            data= self.df.select_dtypes(include="number").corr(),
            annot=True,
            fmt=".2f",
            ax = ax,
        )
        ax.set_title("Correlation Heatmap")
        plt.tight_layout()
        plt.show()


