from src.config.database import property_information_collection
from src.config.database import  property_forecast_collection
from bson import ObjectId

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
        document = self.property_info.find_one({"user_id":self.user_id, "property_id":ObjectId(self.property_id)})
        units_information = document["property_information"]
        return units_information
    
    def units_info(self):
        units_information = self.units_base_info()
        units_information_totals = {"actual_rent": [], "new_rent": [], "vacant_units": [], "total_units":[], "total_sqft":[]}

        for units_information_concept in units_information["units_information"]:
            actual = units_information_concept["amount_units"] * units_information_concept["actual_month_rent"]
            new = units_information_concept["amount_units"] * units_information_concept["new_month_rent"]
            size = units_information_concept["amount_units"] * units_information_concept["size"]

            units_information_totals["total_sqft"].append(size)
            units_information_totals["actual_rent"].append(actual)
            units_information_totals["new_rent"].append(new)
            units_information_totals["vacant_units"].append(units_information_concept["vacant"])
            units_information_totals["total_units"].append(units_information_concept["amount_units"])
        return units_information_totals

    def expense_input_info(self):
        #information entered by user in property information initial payload from expense section.
        document = self.property_info.find_one({"user_id":self.user_id, "property_id":ObjectId(self.property_id)})
        property_expense_information = document["expense"]
        return property_expense_information

    def capital_input_info(self):
        #information entered by user in property information initial payload from capital section.
        document = self.property_info.find_one({"user_id":self.user_id, "property_id":ObjectId(self.property_id)})
        property_capital_information = document["capital"]
        return property_capital_information