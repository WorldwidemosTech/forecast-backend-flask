from src.config.database import property_information_collection
from src.config.database import  property_forecast_collection

class Property():
     #information entered by user in property information initial payload from section called general data in the frontend
     #but in the json payload it is called property information as well, it means the name is repeated (just to avoid confusion).
    
    def __init__(self, user_id, property_id):
        self.property_info = property_information_collection
        self.property_forecast = property_forecast_collection
        self.user_id = user_id
        self.property_id = property_id

    def units_base_info(self):
        #information enter by user in property information initial payload from section called units information.
        document = self.property_info.find_one({"user_id":self.user_id, "property_id":self.property_id})
        units_information = document["property_information"]
        return units_information
    
    def units_info(self):
        units_information = self.units_base_info()
        total_rent = {"actual": [], "new": [], "vacant": [], "total_units":[]}

        for rent in units_information["units_information"]:
            actual = rent["amount_units"] * rent["actual_month_rent"]
            new = rent["amount_units"] * rent["new_month_rent"]
            total_rent["actual"].append(actual)
            total_rent["new"].append(new)
            total_rent["vacant"].append(rent["vacant"])
            total_rent["total_units"].append(rent["amount_units"])
        return total_rent

    def expense_input_info(self):
        #information entered by user in property information initial payload from expense section.
        document = self.property_info.find_one({"user_id":self.user_id, "property_id":self.property_id})
        property_expense_information = document["expense"]
        return property_expense_information

        