import json
from src.config.database import property_information_collection
from bson import ObjectId
import pandas as pd
from post_xlsx_s3 import post_to_s3



def fromJSON_toXLSX(json_forecast):
    """Receive all the forecast values as a JSON, parse the sections, 
            values and convert them into a XLSX """

    json_forecast_dict = json.load(json_forecast)
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
        income.to_excel(document, sheet_name="Income", index=True)
        capital.to_excel(document, sheet_name="Capital", index=True)
        expense.to_excel(document, sheet_name="Expense", index=False)
        expense_totals_df.to_excel(document, sheet_name="Expense totals", index=True)
        management_expense_df.to_excel(document, sheet_name="Expense management", index=True)
        summary.to_excel(document, sheet_name="Summary", index=True)
