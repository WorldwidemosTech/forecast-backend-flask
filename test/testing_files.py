from pydoc import doc
from bson import ObjectId
from src.config.database import property_information_collection as property_info
from bson.json_util import dumps
import json

document = property_info.find_one({"user_id":"cs5XxWGIbnRQBAbnt1ugSxBYMd03", "property_id":ObjectId("6352d31e93d134950bbaf4cf")})
#units_information = document["_id"]
document  = document

print(type(document))

# expense_schema = {}

# expense_schema["management_expenses"] = {}

# expense_schema["management_expenses"].update({"office_supplies_total_sq":[], "office_supplies_total_units":[]})

# print(expense_schema)

