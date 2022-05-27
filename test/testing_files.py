from src.config.database import property_information_collection as property_info

document = property_info.find_one({"user_id":"dlopezvsr", "property_id":"6223cf8c40b07aaf6c4f36b1"})
units_information = document["property_information"]
print(units_information)