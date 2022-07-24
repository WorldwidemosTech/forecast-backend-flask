"""from src.config.database import property_information_collection as property_info
income_schema = {}
document = property_info.find_one({"user_id":"dlopezvsr", "property_id":"6223cf8c40b07aaf6c4f36b1"})
units_information = document["income"]

for income_concepts in document["income"]:
    income_schema[income_concepts] = document["income"][income_concepts]"""


"""utility_expenses = {
    "electricity":630,
    "water": 11920,
    "trash":710,
    "gas":1180
    }

for item in utility_expenses:
    print(utility_expenses[item])
"""
import numpy as np
import pandas as pd

list_of_utilities = np.array([[2,3,4]])
listo = np.array([[1,2,3]])


print(np.subtract(listo, list_of_utilities))

