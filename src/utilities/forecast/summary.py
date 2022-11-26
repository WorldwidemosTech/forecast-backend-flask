from re import U
from src.config.database import property_information_collection
from src.config.database import  property_forecast_collection
from src.utilities.forecast.property_information import Property

class Summary(Property):
    
    def __init__(self, user_id, property_id):
        Property.__init__(self, user_id, property_id)
        self.property_info = property_information_collection
        self.property_forecast = property_forecast_collection
        self.summary_schema = {}
        self.summary_schema_post = {"summary": self.summary_schema}

        self.total_unit_sqft = sum(Property.units_info(self)["total_sqft"])
        self.amount_units = sum(Property.units_info(self)["total_units"])
    
    def execute(self):
        
        self.output_info()
        self.summary_values()
        self.property_forecast.update_one({"property_id": self.property_id,
                                            "user_id":self.user_id},
                                            {"$set":self.summary_schema_post})
        return  self.summary_schema_post

    
    def output_info(self):
        #Information calculated on income module needed to calculate expense concepts
        document = self.property_forecast.find_one({"user_id":self.user_id, "property_id":self.property_id})
        return document

    def summary_values(self):
        #this function will calculate the per unit and per sqft values of every big total inside 
        #each section (capital, income, expense).
        digits = 2
        net_cash_flow_per_unit = sum(self.output_info()["expense"]["expense_totals"]["net_cash_flow"]) / self.amount_units
        net_cash_flow_per_sqft = sum(self.output_info()["expense"]["expense_totals"]["net_cash_flow"]) / self.total_unit_sqft
        self.summary_schema["net_cash_flow"] = {"per_unit": round(net_cash_flow_per_unit, digits), "per_sqft":round(net_cash_flow_per_sqft, digits)}

        net_operating_income_per_unit = sum(self.output_info()["expense"]["expense_totals"]["net_operating_income_pre_capital"]) / self.amount_units
        net_operating_income_per_sqft = sum(self.output_info()["expense"]["expense_totals"]["net_operating_income_pre_capital"]) / self.total_unit_sqft
        self.summary_schema["net_operating_income_pre_capital"] = {"per_unit": round(net_operating_income_per_unit, digits), "per_sqft":round(net_operating_income_per_sqft, digits)}
        
        capital_expenses_per_unit = sum(self.output_info()["capital"]["capital_expenditures"]) / self.amount_units
        capital_expenses_per_sqft = sum(self.output_info()["capital"]["capital_expenditures"]) / self.total_unit_sqft
        self.summary_schema["capital_expenditures"] = {"per_unit": round(capital_expenses_per_unit, digits), "per_sqft":round(capital_expenses_per_sqft, digits)}

        total_management_expenses_per_unit = sum(self.output_info()["expense"]["expense_totals"]["total_management_expenses"]) / self.amount_units
        total_management_expenses_per_sqft = sum(self.output_info()["expense"]["expense_totals"]["total_management_expenses"]) / self.total_unit_sqft
        self.summary_schema["total_management_expenses"] = {"per_unit": round(total_management_expenses_per_unit, digits), "per_sqft":round(total_management_expenses_per_sqft, digits)}
        
        total_utility_expenses_per_unit = self.output_info()["expense"]["total_utility_expenses"][0] / self.amount_units
        total_utility_expenses_per_sqft = self.output_info()["expense"]["total_utility_expenses"][0] / self.total_unit_sqft
        self.summary_schema["total_utility_expenses"] = {"per_unit": round(total_utility_expenses_per_unit, digits), "per_sqft":round(total_utility_expenses_per_sqft, digits)}

        employees_salary_expense_per_unit = self.output_info()["expense"]["employees_salary_expense"][0] / self.amount_units
        employees_salary_expense_per_sqft = self.output_info()["expense"]["employees_salary_expense"][0] / self.total_unit_sqft
        self.summary_schema["employees_salary_expense"] = {"per_unit": round(employees_salary_expense_per_unit, digits), "per_sqft":round(employees_salary_expense_per_sqft, digits)}
        
        total_maintenance_expenses_per_unit = self.output_info()["expense"]["total_maintenance_expenses"][0] / self.amount_units
        total_maintenance_expenses_per_sqft = self.output_info()["expense"]["total_maintenance_expenses"][0] / self.total_unit_sqft
        self.summary_schema["total_maintenance_expenses"] = {"per_unit": round(total_maintenance_expenses_per_unit, digits), "per_sqft":round(total_maintenance_expenses_per_sqft, digits)}
        
        operating_expenses_per_unit = sum(self.output_info()["expense"]["expense_totals"]["total_operating_expenses"]) / self.amount_units
        operating_expenses_per_sqft = sum(self.output_info()["expense"]["expense_totals"]["total_operating_expenses"]) / self.total_unit_sqft
        self.summary_schema["total_operating_expenses"] = {"per_unit": round(operating_expenses_per_unit, digits), "per_sqft":round(operating_expenses_per_sqft, digits)}

        self.summary_schema["big_totals_summary"] = {
            "expense_big_total": sum(self.output_info()["expense"]["expense_totals"]["total_operating_expenses"]),
            "income_big_total": sum(self.output_info()["income"]["big_total_income"]),
            "net_cash_flow": sum(self.output_info()["expense"]["expense_totals"]["net_cash_flow"]),
            "total_maintenance_expenses":self.output_info()["expense"]["total_maintenance_expenses"][0],
            "employees_salary_expense":self.output_info()["expense"]["employees_salary_expense"][0],
            "total_utility_expenses":self.output_info()["expense"]["total_utility_expenses"][0],
            "total_management_expenses":sum(self.output_info()["expense"]["expense_totals"]["total_management_expenses"]),
            "capital_expenditures":sum(self.output_info()["capital"]["capital_expenditures"])
        }



'''def main():
    summary = Summary("dlopezvsr", "62e851b0c710e7c50f913e14")
    print(summary.execute())

if __name__ == "__main__":
    main()'''