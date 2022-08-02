from re import U
from src.config.database import property_information_collection
from src.config.database import  property_forecast_collection
from src.utilities.forecast.property_information import Property
import numpy as np

class Expense(Property):
    
    def __init__(self, user_id, property_id):
        Property.__init__(self, user_id, property_id)
        self.property_info = property_information_collection
        self.property_forecast = property_forecast_collection
        self.expense_schema = {}
        self.expense_schema_post = {"expense": self.expense_schema}
    
    def execute(self):
        
        self.income_output_info()
        self.management_fee()
        self.advertising()
        self.misc_management_expense()
        self.total_management_expense()
        self.employee_insurance()
        self.payroll_fee()
        self.payroll_tax()
        self.worker_compensation()
        self.property_insurance()
        self.utility_expense()
        self.maintenance_expense()   
        self.total_operating_expenses()   
        self.et_operating_income_pre_capital() 
        self.net_cash_flow()
        self.property_forecast.update_one({"property_id": self.property_id,
                                            "user_id":self.user_id},
                                            {"$push":self.expense_schema_post})

        return  self.expense_schema_post
    
    def income_output_info(self):
        #Information calculated on income module needed to calculate expense concepts
        document = self.property_forecast.find_one({"user_id":self.user_id, "property_id":self.property_id})
        income_info = document["income"]
        return income_info

    def capital_output_info(self):
        #Information calculated on capital module needed to calculate expense concepts
        document = self.property_forecast.find_one({"user_id":self.user_id, "property_id":self.property_id})
        capital_info = document["capital"]
        return capital_info

    def management_fee(self):
        #time series type value
        expense_inputs = Property.expense_input_info(self)
        income_outputs = self.income_output_info()
        self.expense_schema["management_expenses"]["management_fee"] = []
        for month in range(12):
            self.expense_schema["management_expenses"]["management_fee"].append(round(income_outputs["big_total_income"][month] * expense_inputs["management_fee_percentage"]))

    def advertising(self):
        #unique type value
        expense_inputs = Property.expense_input_info(self)
        units = Property.units_info(self)
        self.expense_schema["management_expenses"]["advertising"] = [sum(units["total_units"]) * expense_inputs["marketing_fee_per_unit"]]
    
    def misc_management_expense(self):
        #unique type values 
        units = sum(Property.units_info(self)["total_units"])
        expense_inputs = Property.expense_input_info(self)
        self.expense_schema["management_expenses"]["office_supplies_total_units"] = [expense_inputs["office_supplies_per_unit"] * units]
        self.expense_schema["management_expenses"]["accounting_software_suscriptions"] = [expense_inputs["accounting_software_suscriptions_per_unit"] * units]
        self.expense_schema["management_expenses"]["website_maintenance"] = [expense_inputs["website_maintenance"]]
        self.expense_schema["management_expenses"]["banking"] = [expense_inputs["banking"]] 
        self.expense_schema["management_expenses"]["legal_and_accounting"] = [expense_inputs["legal_and_accounting"]]
        self.expense_schema["management_expenses"]["internet_computers"] = [expense_inputs["internet_computers"]]
        self.expense_schema["management_expenses"]["total_miscellaneous_management_fees"] = [expense_inputs["miscellaneous_management_fees_per_unit"] * units]
    
    def total_management_expense(self):
        management_expenses = []
        #there are some values that are the same each month that need to be added to the ones that vary each month
        for management_expense_json_key in self.expense_schema["management_expenses"]:
            time_series_concept = self.expense_schema["management_expenses"][management_expense_json_key]
            
            if len(time_series_concept) == 1:
                for value in range(11):
                    self.expense_schema["management_expenses"][management_expense_json_key].append(time_series_concept[0])
                management_expenses.append(self.expense_schema["management_expenses"][management_expense_json_key])
            else:
                management_expenses.append(time_series_concept)
        #the variable below is first converting a list of lists into an array, afer that we are summing all the values column by column and...
        #finally retrieving the total values of the array summed month by month converted into a list.
        sum_management_expenses_time_series = np.ndarray.tolist(
            np.sum(np.array(
                management_expenses), axis=0))

        self.expense_schema["total_management_expenses"] = sum_management_expenses_time_series


    def employee_expense(self):
        expense_inputs = Property.expense_input_info(self)
        employee_info = {"employees_salary":[], "total_employees":[]}
        
        for employees in expense_inputs["employee_expense"]:
            employee_info["employees_salary"].append(employees["hourly_rate"] * employees["monthly_hours"] * employees["number_eployees"])
            employee_info["total_employees"].append(employees["number_eployees"])

        self.expense_schema["employees_salary_expense"] = [sum(employee_info["employees_salary"])]
        self.expense_schema["total_number_employees"] = [sum(employee_info["total_employees"])]
    
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

    def utility_expense(self):
        #it is a time series with same value for each month
        expense_inputs = Property.expense_input_info(self)
        utility_expenses = expense_inputs["utility_expense"]
        list_of_utilities = []
        for item in utility_expenses:
            list_of_utilities.append(utility_expenses[item])
        
        list_of_utilities_sum = [sum(list_of_utilities)]
        self.expense_schema["total_utility_expenses"] = list_of_utilities_sum
        return list_of_utilities_sum
    
    def maintenance_expense(self): 
        # Create a function to calculate the maintenance expense once we divide it by different concepts, in the meantime
        # we will just ask the user for one big total
        maintenance_expenses =  [Property.expense_input_info(self)["maintenance_expense"]] 
        self.expense_schema["total_maintenance_expenses"] = maintenance_expenses

    def convert_to_time_series(self):
        #Convert a single item list to a time series list with the same value for each month to facilitate the calculations
        
        pass

    def total_operating_expenses(self):
  
        management_expense = self.expense_schema["total_management_expenses"]
        utility_expenses = self.utility_expense()
        employee_expenses = self.expense_schema["employees_salary_expense"]
        #maintenance expense is a value entered by the user as a total value, in the 2.0 version we can breakdown the concepts
        maintenance_expenses =  [Property.expense_input_info(self)["maintenance_expense"]]
        fixed_expenses = [Property.expense_input_info(self)["realstate_taxes"] + self.expense_schema["property_insurance"]]
        
        self.expense_schema["total_operating_expenses"] = []
        for month in range(12):
            self.expense_schema["total_operating_expenses"].append(management_expense[month] + utility_expenses[0] + employee_expenses[0] + maintenance_expenses[0] + fixed_expenses[0])

    def net_operating_income_pre_capital(self):
        # JSON retrived from database in order to get the value of total income preciously calculated in income class
        income_schema = self.income_output_info()
        total_income = income_schema["big_total_income"]
        total_income_array = np.array([total_income])
        total_operating_expenses_array = np.array([self.expense_schema["total_operating_expenses"]])

        self.expense_schema["net_operating_income_pre_capital"] = np.ndarray.tolist(np.subtract(total_income_array, total_operating_expenses_array))

    def net_cash_flow(self):
        capital_expenses = self.capital_output_info()["capital_expenditures"]
        net_operating_array = np.array([capital_expenses])
        capital_expenditures_array = np.array([self.capital_schema["capital_expenditures"]])
        self.expense_schema["net_cash_flow"] = np.ndarray.tolist(np.subtract(net_operating_array, capital_expenditures_array))
    
    
def main():
    expense = Expense("dlopezvsr", "6223cf8c40b07aaf6c4f36b1")
    print(expense.execute())

if __name__ == "__main__":
    main()