import json
from src.config.database import property_information_collection
from bson import ObjectId
import pandas as pd



def fromJSON_toXLSX(json_forecast):
    json_forecast_dict = json.load(json_forecast)
    # TODO: fix monthly moveouts from forecast brain, it needs to be the same length
    # TODO: test expense and fix in case arrays do not have the same length
    management_expense = json_forecast_dict["expense"]["management_expenses"]
    expense_totals = json_forecast_dict["expense"]["expense_totals"]

    json_forecast_dict["expense"].pop("management_expenses")
    json_forecast_dict["expense"].pop("expense_totals")
 

    income = pd.DataFrame(data=json_forecast_dict["income"])
    capital = pd.DataFrame(data=json_forecast_dict["capital"])
    expense = pd.DataFrame(data=json_forecast_dict["expense"])
    expense_totals_df = pd.DataFrame(data=expense_totals)
    management_expense_df = pd.DataFrame(data=management_expense)

    summary = pd.DataFrame(data=json_forecast_dict["summary"])
    

    with pd.ExcelWriter("forecast.xlsx") as document:
        income.to_excel(document, sheet_name="Income", index=False)
        capital.to_excel(document, sheet_name="Capital", index=False)
        expense.to_excel(document, sheet_name="Expense", index=False)
        expense_totals_df.to_excel(document, sheet_name="Expense totals", index=False)
        management_expense_df.to_excel(document, sheet_name="Expense management", index=False)
        summary.to_excel(document, sheet_name="Summary", index=False)


file_json = open("/Users/diegolopez/Documents/PROJECTS/MOSTECH/forecast-backend-flask/src/utilities/test.json")
fromJSON_toXLSX(file_json)