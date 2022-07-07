from re import U
from src.config.database import property_information_collection
from src.config.database import  property_forecast_collection
from src.utilities.forecast.property_information import Property

class Expense(Property):
    
    def __init__(self, user_id, property_id):
        Property.__init__(self, user_id, property_id)
        self.property_info = property_information_collection
        self.property_forecast = property_forecast_collection
        self.expense_schema = {}
        self.expense_schema_post = {"expense": self.expense_schema}
    
    def execute(self):
        # TODO: Add to the end
        """self.property_forecast.update_one({"property_id": self.property_id,
                                            "user_id":self.user_id},
                                            {"$push":self.expense_schema_post})"""
        self.income_output_info()
        self.management_fee()
        self.advertising()
        self.misc_management_expense()
        return  self.expense_schema_post
    
    def income_output_info(self):
        #Information calculated on income module needed to calculate expnse concepts
        document = self.property_forecast.find_one({"user_id":self.user_id, "property_id":self.property_id})
        income_info = document["income"]
        return income_info

    def management_fee(self):
        expense_inputs = Property.expense_input_info(self)
        income_outputs = self.income_output_info()
        self.expense_schema["management_fee"] = []
        for month in range(12):
            self.expense_schema["management_fee"].append(round(income_outputs["big_total_income"][month] * expense_inputs["management_fee_percentage"]))

    def advertising(self):
        expense_inputs = Property.expense_input_info(self)
        units = Property.units_info(self)
        self.expense_schema["advertising"] = [sum(units["total_units"]) * expense_inputs["marketing_fee_per_unit"]]
    
    def misc_management_expense(self):
        units = sum(Property.units_info(self)["total_units"])
        expense_inputs = Property.expense_input_info(self)
        self.expense_schema["office_supplies_per_unit"] = expense_inputs["office_supplies_per_unit"] * units
        self.expense_schema["accounting_software_suscriptions_per_unit"] = expense_inputs["accounting_software_suscriptions_per_unit"] * units
        self.expense_schema["telephone"] = expense_inputs["telephone"]
        self.expense_schema["website_maintenance"] = expense_inputs["website_maintenance"]
        self.expense_schema["banking"] = expense_inputs["banking"] 
        self.expense_schema["legal_and_accounting"] = expense_inputs["legal_and_accounting"]
        self.expense_schema["internet_computers"] = expense_inputs["internet_computers"]
        self.expense_schema["miscellaneous_management_fees_per_unit"] = expense_inputs["miscellaneous_management_fees_per_unit"] * units
    
    def employee_expense(self):
        expense_inputs = Property.expense_input_info(self)
        employee_info = {"employees_salary":[], "total_employees":[]}
        
        for employees in expense_inputs["employee_expense"]:
            employee_info["employees_salary"].append(employees["hourly_rate"] * employees["monthly_hours"] * employees["number_eployees"])
            employee_info["total_employees"].append(employees["number_eployees"])

        self.expense_schema["employees_salary_expense"] = sum(employee_info["employees_salary"])
        self.expense_schema["total_number_employees"] = sum(employee_info["total_employees"])
    
    def employee_insurance(self):
        expense_inputs = Property.expense_input_info(self)
        self.expense_schema["health_insurance"] = expense_inputs["employee_insurance_percentage"] * self.expense_schema["employees_salary_expense"]

    def payroll_fee(self):
        expense_inputs = Property.expense_input_info(self)
        self.expense_schema["payroll_fees"] = expense_inputs["payroll_fee_per_employee"] * self.expense_schema["total_number_employees"]

    def payroll_tax(self):
        expense_inputs = Property.expense_input_info(self)
        self.expense_schema["payroll_tax"] = expense_inputs["payroll_tax_percentage"] * self.expense_schema["employees_salary_expense"]

    def worker_compensation(self):
        expense_inputs = Property.expense_input_info(self)
        self.expense_schema["worker_compensation"] = expense_inputs["workers_compensation_percentage"] * (self.expense_schema["health_insurance"]+self.expense_schema["employees_salary_expense"])
       
    def property_insurance(self):
        expense_inputs = Property.expense_input_info(self)
        units = sum(Property.units_info(self)["total_units"])
        self.expense_schema["property_insurance"] = round(expense_inputs["insurance_per_unit"] * units)/12




def main():
    expense = Expense("dlopezvsr", "6223cf8c40b07aaf6c4f36b1")
    print(expense.execute())

if __name__ == "__main__":
    main()