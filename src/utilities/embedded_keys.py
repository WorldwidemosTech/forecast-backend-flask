from src.config.logger import logger
from src.config.database import property_information_collection
from bson import ObjectId


def subkeys_processor(data, query, property_id, user_id):
    """ This funtion will handle and process every modification applied to the corresponding forecast section
    without overwriting the information in Mongo """

    section = list(data.keys())[0]
    pre_data = property_information_collection.find_one({'property_id': ObjectId(property_id),
                                                     'user_id': user_id})
    logger.info(pre_data)

    if section == 'property_information':
        try:
            response = property_information_collection.update_one(query, {
                '$set': {"property_information": data['property_information']}})
            property_information_collection.update_one(query, {
                '$set': {"property_information.units_information": pre_data['property_information']['units_information']}})
        except:
            response = property_information_collection.update_one(query, {
                '$set': {"property_information": data['property_information']}})

        return response

    if section == 'units_information':
        response = property_information_collection.update_one(query, {
            '$set': {"property_information.units_information": data['units_information']}})
        return response

    if section == 'expense':
        try:
            response = property_information_collection.update_one(query, {'$set': {"expense": data['expense']}})
            property_information_collection.update_one(query, {
                '$set': {"expense.utility_expenses": pre_data['expense']['utility_expenses']}})
            property_information_collection.update_one(query, {
                '$set': {"expense.employee_expense": pre_data['expense']['employee_expense']}})
        except:
            response = property_information_collection.update_one(query, {
                '$set': {"expense": data['expense']}})

        return response

    if section == 'utility_expenses':
        response = property_information_collection.update_one(query, {
            '$set': {"expense.utility_expenses": data['utility_expenses']}})

        return response

    if section == 'employee_expense':
        response = property_information_collection.update_one(query, {
            '$set': {"expense.employee_expense": data['employee_expense']}})
    
    else:
        response = property_information_collection.update_one(query, {'$set': data})
            
        return response

