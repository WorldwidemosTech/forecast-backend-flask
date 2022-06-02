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
        """self.property_forecast.update_one({"property_id": self.property_id,
                                            "user_id":self.user_id},
                                            {"$push":self.expense_schema_post})"""
        self.income_output_info()
        self.management_fee()
        self.advertising()
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
        


        

def main():
    expense = Expense("dlopezvsr", "6223cf8c40b07aaf6c4f36b1")
    print(expense.execute())

if __name__ == "__main__":
    main()