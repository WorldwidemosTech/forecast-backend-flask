from src.config.database import property_information_collection


pre_data = property_information_collection.find_one({'property_id': '62e851b0c710e7c50f913e14',
                                                     'user_id': 'dlopezvsr'})


print(pre_data)