from src.config.database import property_information_collection as property_info
income_schema = {}
document = property_info.find_one({"user_id":"dlopezvsr", "property_id":"6223cf8c40b07aaf6c4f36b1"})
units_information = document["income"]

for income_concepts in document["income"]:
    income_schema[income_concepts] = document["income"][income_concepts]

print(income_schema)
print(units_information)