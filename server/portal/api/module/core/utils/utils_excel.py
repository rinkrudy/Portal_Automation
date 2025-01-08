import pandas as pd

class Utils_Excel:
    def read_excel(file_path, sheet_name, start_row_index = 0):
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=start_row_index)
        return df

    def save_excel(file_path, sheet_name, dt_src):
        excel_writer = pd.ExcelWriter(file_path, engine='openpyxl')
        dt_src.to_excel(excel_writer, sheet_name = sheet_name, index= False)
        excel_writer._save()

 