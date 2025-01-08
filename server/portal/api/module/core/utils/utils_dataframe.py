import pandas as pd

class Utils_DataFrame:
    def add_columns(df, column_names, initial_value):
        for name in column_names:
            if name not in df.add_columns:
                df[name] = initial_value