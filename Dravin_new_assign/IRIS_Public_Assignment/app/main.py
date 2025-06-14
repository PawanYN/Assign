from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

# Read the Excel file once when the app starts
try:
    df = pd.read_excel("Data/capbudg.xlsx")

    tables = {
        "INITIAL INVESTMENT": df.iloc[2:9, 0:3].dropna(how="all", axis=1),
        "CASHFLOW DETAILS": df.iloc[2:6, 4:7].dropna(how="all", axis=1),
        "DISCOUNT RATE": df.iloc[2:11, 8:11].dropna(how="all", axis=1),
        "WORKING CAPITAL": df.iloc[11:14, 0:3].dropna(how="all", axis=1),
        "GROWTH RATES": df.iloc[16:19, 0:12].dropna(how="all", axis=1),
        "INITIAL INVESTMENT2": df.iloc[21:30, 0:2].dropna(how="all", axis=1),
        "SALVAGE VALUE": df.iloc[32:34, 0:11].dropna(how="all", axis=1),
        "OPERATING CASHFLOWS": df.iloc[36:49, 0:11].dropna(how="all", axis=1),
        "Investment Measures": df.iloc[52:55, 1:3].dropna(how="all", axis=1),
        "BOOK VALUE & DEPRECIATION": df.iloc[58:61, 0:11].dropna(how="all", axis=1),
    }

except Exception as e:
    print(f"Error loading Excel file: {e}")
    tables = {}



#------------------ rough work-----------------------------
name=[key for key in tables]
print(name)

row_names = [m for m in tables["INITIAL INVESTMENT"].iloc[:, 0]]
print(row_names)



#------------------------------------------------------------------------
#                        All Questions are answered below
#------------------------------------------------------------------------


@app.get("/")
def root():
    return  "Server running successfully"

@app.get("/list_tables")
def list_tables():
    return {"tables": list(tables.keys())}

@app.get("/get_table_details/{item_name}")
def get_table_detail(item_name:str):
    row_names = [m for m in tables[item_name].iloc[:, 0]]
    return {"table name": item_name, "row_names":row_names}

@app.get("/row_sum/{table_name}/{row_name}")
def row_sum(table_name: str ,row_name: str ):
    row_data = tables[table_name][tables[table_name].iloc[:, 0] == row_name].iloc[0, 1:]
    return row_data.sum()

