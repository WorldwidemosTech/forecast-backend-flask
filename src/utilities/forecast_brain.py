from src.config.database import property_scenarios_collection
from src.config.database import property_information_collection


class Brain():

    def __init__(self):
        self.property_info = property_information_collection
        self.property_scenarios = property_scenarios_collection

    def execute(self):
        self.forecast_capital()
        self.forecast_income()
        self.forecast_expenses()
    
    def property_information(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        information = document["prperty_information"]

    def forecast_capital(self, user_id, property_id):
        ...
    
    def forecast_income(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        units_information = document["prperty_information"]
        total_rent = {
            "actual": [],
            "new": []
        }
        #scheduled rent is same that actual rent, and Current Gross Rent Potential
        scheduled_rent = sum(total_rent["actual"])

        for rent in units_information["units_information"]:
            actual = rent["amount_units"] * rent["actual_month_rent"]
            new = rent["amount_units"] * rent["new_month_rent"]
            total_rent["actual"].append(actual)
            total_rent["new"].append(new)

        average_monthly_increase_grp = (sum(total_rent["new"]) - scheduled_rent)/12
        gross_rent_potential = scheduled_rent + average_monthly_increase_grp
        grp_time_series = [gross_rent_potential]
        for month in range(11):
            grp_time_series.append(gross_rent_potential + grp_time_series[month])

        #Here starts actual status formulas
        amount_units = units_information["units_information"]["amount_units"]
        turnover = units_information["turnover"]

        #Estimated Turnover is the sum of all the months of montlhy_moveouts
        montlhy_moveouts = round(amount_units * turnover/12)

        actual_status = (1/(amount_units - units_information["units_information"]["vacant"])) * amount_units
        current_loss_to_lease = -(scheduled_rent-actual_status)
        current_actual_rent = scheduled_rent + current_loss_to_lease

        # TODO: porcentaje pendiente a confirmar con Ricardo
        per_unit_rent_growth_renewal = (scheduled_rent * .02) / amount_units

        actual_status_estimated = current_actual_rent

        average_monthly_increase_actual = current_actual_rent + actual_status_estimated




    
    def forecast_expenses(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        document = document["expense"]
        for key in document:
            for subconcept in key:
                ...



