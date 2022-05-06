from src.config.database import property_scenarios_collection
from src.config.database import property_information_collection


class Brain():

    def __init__(self):
        self.property_info = property_information_collection
        self.property_scenarios = property_scenarios_collection

    def execute(self):
        self.forecast_capital()
        self.forecast_income()
        self.forecast_expenses()

    def forecast_capital(self, user_id, property_id):
        ...
    
    def forecast_income(self, user_id, property_id):
        ...
    
    def forecast_expenses(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        ducument = document["expense"]

