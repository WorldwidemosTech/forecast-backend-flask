from re import U
from src.config.database import property_information_collection
from src.config.database import  property_forecast_collection
from src.utilities.forecast.property_information import Property
import numpy as np

class Capital(Property):
    
    def __init__(self, user_id, property_id):
        Property.__init__(self, user_id, property_id)
        self.property_info = property_information_collection
        self.property_forecast = property_forecast_collection
        self.capital_schema = {}
        self.schema_post = {"capital:": self.capital_schema}
    
    def execute(self):
        # TODO: Add to the end
        """self.property_forecast.update_one({"property_id": self.property_id,
                                            "user_id":self.user_id},
                                            {"$push":self.schema_post})"""
        self.capital_expenditures()
        
        return self.capital_schema()
    
    def capital_expenditures(self):
        capital_expenditures = Property.capital_input_info(self)
        monthly_capital_expenditures = [capital_expenditures["total_year_amount"] / 12]
        for i in range(11):
            monthly_capital_expenditures.append(monthly_capital_expenditures[0])

        self.capital_schema["capital_expenditures"] = monthly_capital_expenditures