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
        units_information = document["property_information"]
        total_rent = {
            "actual": [],
            "new": [],
            "vacant": []
        }
        #scheduled rent is same that actual rent, and Current Gross Rent Potential
        scheduled_rent = sum(total_rent["actual"])
        #scheduled_new_rent is also Proposed Gross Rent Potential
        scheduled_new_rent = sum(total_rent["new"])
        vacant_units = sum(total_rent["vacant"])

        for rent in units_information["units_information"]:
            actual = rent["amount_units"] * rent["actual_month_rent"]
            new = rent["amount_units"] * rent["new_month_rent"]
            total_rent["actual"].append(actual)
            total_rent["new"].append(new)
            total_rent["vacant"].append(rent["vacant"])

        average_monthly_increase_grp = (scheduled_new_rent - scheduled_rent)/12
        gross_rent_potential = scheduled_rent + average_monthly_increase_grp
        #Needs to be returned
        grp_time_series = [gross_rent_potential]
        for month in range(11):
            grp_time_series.append(gross_rent_potential + grp_time_series[month])

        #Here starts actual status formulas
        amount_units = units_information["units_information"]["amount_units"]
        turnover = units_information["turnover"]
        monthly_moveouts = round(amount_units * turnover/12)
        actual_status = (1/(amount_units - vacant_units)) * amount_units
        current_loss_to_lease = -(scheduled_rent-actual_status)
        current_actual_rent = scheduled_rent + current_loss_to_lease
        per_unit_rent_growth_market = (scheduled_new_rent - current_actual_rent) / amount_units
        # TODO: porcentaje pendiente a confirmar con Ricardo
        per_unit_rent_growth_renewal = (scheduled_rent * .02) / amount_units
        
        #The estimated turnover is the sum of all the months of montlhy_moveouts
        actual_rent_growth_market = (monthly_moveouts*12) * per_unit_rent_growth_market
        actual_rent_growth_existing = (amount_units - (monthly_moveouts*12)) * per_unit_rent_growth_renewal
        actual_status_estimated = current_actual_rent + actual_rent_growth_market + actual_rent_growth_existing 
        average_monthly_increase_actual = (actual_status_estimated - current_actual_rent)/12
        actual_status_timeseries = actual_status + average_monthly_increase_actual
        
        #Needs to be returned
        actual_status_timeseries_list = [actual_status_timeseries]
        for month in range(11):
            actual_status_timeseries_list.append(actual_status_timeseries + actual_status_timeseries_list[month])

        occupancy_goals_precentage = ((amount_units - vacant_units)/amount_units)*100
        #Needs to be returned
        occupancy_goals_list = [occupancy_goals_precentage]

        # TODO: improve ocupancy goals formula, no me convence
        for month in range(11):
            if occupancy_goals_precentage < 94:
                occupancy_goals_precentage += (occupancy_goals_precentage * .01)
            else:
                occupancy_goals_precentage = 95
            occupancy_goals_list.append(round(occupancy_goals_precentage,2))

        #Needs to be returned
        loss_gain_lease_list = []
        for month in range(12):
            loss_gain_lease = actual_status_timeseries_list[month] - grp_time_series[month]
            loss_gain_lease_list.append(loss_gain_lease)

        #Needs to be returned
        occuppied_units_list = []
        vacant_units_list = []
        for month in range(12):
            occupied_units = occupancy_goals_list[month] * amount_units
            occuppied_units_list.append(occupied_units)
            vacant_units_list.append(amount_units - occupied_units)

        #Needs to be returned
        #All the values needs to be presented as negative
        vacancy_loss_list = []
        concessions_list = []
        write_offs_list = []
        for month in range(12):
            vacancy_loss = (actual_status_timeseries_list[month]/occuppied_units_list[month])*vacant_units_list[month]
            vacancy_loss_list.append(vacancy_loss)
            concessions_list.append(actual_status_timeseries_list[month] * units_information["concessions"])
            write_offs_list.append(actual_status_timeseries_list[month] * units_information["write_offs"])



    def forecast_expenses(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        document = document["expense"]
        for key in document:
            for subconcept in key:
                ...



