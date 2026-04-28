import pandas as pd

class DataLoader:
    """
    Loads and validates a CSV file uploaded by user, and exposes basic profile information.
    """
    def __init__(self, file):
        """
        Stores the uploaded file.
        """
        self.uploaded_file = file
        self.df = None

    def is_valid(self) -> bool :
        """
        Checks file is not None and file extension is .csv.
        """
        is_not_none = self.uploaded_file is not None
        if is_not_none and self.uploaded_file.name.endswith(".csv"):
            return True
        else:
            return False

    def load(self)-> pd.DataFrame | None:
        """
        Method that actually reads and returns the data in DataFrame form.
        """
        if not self.is_valid():
            print("Invalid file. Must be a non-null .csv")
            return None
        try:
            self.df = pd.read_csv(self.uploaded_file)
            return self.df
        except Exception as e:
            print(f"Failed to read file: {e}")
            return None

    def get_basic_profile(self) -> dict | None:
        """
        Compute operations to get shape, null counts and null percentage per column
        """

        if self.df is not None:
            shape = self.df.shape
            null_counts = self.df.isnull().sum().to_dict()
            null_pct = (self.df.isnull().sum()/len(self.df)*100).round(2).to_dict()
            return {
                "shape": shape,
                "null_counts": null_counts,
                "null_pct": null_pct
            }
        else:
            print("Data not loaded. Call load() first.")
            return None

    def get_dtype_summary(self) ->dict | None:
        """
        Responsible for providing the dtype of each column present in uploaded file.
        """
        if self.df is not None:
            return self.df.dtypes.to_dict()
        else:
            print("Data not loaded. Call load() first.")
            return None


