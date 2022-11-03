import pandas as pd
import io

def fromJSON_toXLSX(json_forecast):
    """Receive all the forecast values as a JSON, parse the sections, 
            values and convert them into a XLSX """

    json_forecast_dict = json_forecast
    output = io.BytesIO()

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

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    income.to_excel(writer, sheet_name="Income", index=True)
    capital.to_excel(writer, sheet_name="Capital", index=True)
    expense.to_excel(writer, sheet_name="Expense", index=False)
    expense_totals_df.to_excel(writer, sheet_name="Expense totals", index=True)
    management_expense_df.to_excel(writer, sheet_name="Expense management", index=True)
    summary.to_excel(writer, sheet_name="Summary", index=True)
    writer.save()
    xlsx_data = output.getvalue()

    return (xlsx_data)
