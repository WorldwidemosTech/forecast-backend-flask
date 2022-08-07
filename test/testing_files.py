from pydoc import doc
from bson import ObjectId
from src.config.database import property_information_collection as property_info

"""document = property_info.find_one({"user_id":"dlopezvsr", "property_id":ObjectId("62e851b0c710e7c50f913e14")})
units_information = document["income"]
print(units_information)"""

expense_schema = {}

expense_schema["management_expenses"] = {}

expense_schema["management_expenses"].update({"office_supplies_total_sq":[], "office_supplies_total_units":[]})

print(expense_schema)

