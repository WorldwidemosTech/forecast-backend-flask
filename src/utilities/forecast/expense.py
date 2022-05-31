from re import M
from src.config.database import property_information_collection

class Expense():
    
    def __init__(self):
        self.property_info = property_information_collection
        self.expense_schema = {}
    
    def execute(self, user_id, property_id):
        ...
    
    def units_base_info(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        units_information = document["property_information"]
        return units_information

    def management_fee(self, user_id, property_id):
        units_information = self.units_base_info(user_id, property_id)
        
