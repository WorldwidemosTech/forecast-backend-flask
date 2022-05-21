from src.config.database import property_scenarios_collection
from src.config.database import property_information_collection

class Income():
    
    def __init__(self):
        self.property_info = property_information_collection
        self.property_scenarios = property_scenarios_collection
        self.income_schema = {}
    
    def execute(self, user_id, property_id):
        
        return self.income_schema

    def units_base_info(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        units_information = document["property_information"]
        return units_information
    
    def units_info(self, user_id, property_id):
        units_information = self.units_base_info(user_id, property_id)
        total_rent = {"actual": [], "new": [], "vacant": []}

        for rent in units_information["units_information"]:
            actual = rent["amount_units"] * rent["actual_month_rent"]
            new = rent["amount_units"] * rent["new_month_rent"]
            total_rent["actual"].append(actual)
            total_rent["new"].append(new)
            total_rent["vacant"].append(rent["vacant"])
        return total_rent

    def unit_rents(self, user_id, property_id):
        total_rent = self.units_info(user_id, property_id)
        average_monthly_increase_grp = (sum(total_rent["new"]) - sum(total_rent["actual"]))/12
        gross_rent_potential = sum(total_rent["actual"]) + average_monthly_increase_grp
        
        self.income_schema["gross_rent_potential"] = [gross_rent_potential]
        for month in range(11):
            self.income_schema["gross_rent_potential"].append(gross_rent_potential + self.income_schema["gross_rent_potential"][month])
        
    def actual_status(self, user_id, property_id):
        units_information = self.units_base_info(user_id, property_id)
        total_rent = self.units_info(user_id, property_id)

        amount_units = units_information["units_information"]["amount_units"]
        turnover = units_information["turnover"]
        monthly_moveouts = round(amount_units * turnover/12)
        # TODO: reemplazar el 1 por el input del usuario
        actual_status = (units_information["actual_income"]/(amount_units - sum(total_rent["vacant"]))) * amount_units
        current_loss_to_lease = -(sum(total_rent["actual"])-actual_status)
        current_actual_rent = sum(total_rent["actual"]) + current_loss_to_lease
        per_unit_rent_growth_market = (sum(total_rent["new"]) - current_actual_rent) / amount_units
        per_unit_rent_growth_renewal = (sum(total_rent["actual"]) * .02) / amount_units
        actual_rent_growth_market = (monthly_moveouts*12) * per_unit_rent_growth_market
        actual_rent_growth_existing = (amount_units - (monthly_moveouts*12)) * per_unit_rent_growth_renewal
        actual_status_estimated = current_actual_rent + actual_rent_growth_market + actual_rent_growth_existing 
        average_monthly_increase_actual = (actual_status_estimated - current_actual_rent)/12
        actual_status_timeseries = actual_status + average_monthly_increase_actual

        self.income_schema["actual_status_timeseries_list"] = [actual_status_timeseries]
        for month in range(11):
            self.income_schema["actual_status_timeseries_list"].append(actual_status_timeseries + self.income_schema["actual_status_timeseries_list"][month])

        return amount_units

    def occupancy_goals(self, user_id, property_id):
        
        amount_units = self.actual_status(user_id, property_id)
        total_rent = self.units_info(user_id, property_id)
        occupancy_goals_precentage = ((amount_units - sum(total_rent["vacant"]))/amount_units)*100

        self.income_schema["occupancy_goals_list"] = [occupancy_goals_precentage]

        # TODO: improve ocupancy goals formula, no me convence
        for month in range(11):
            if occupancy_goals_precentage < 94:
                occupancy_goals_precentage += (occupancy_goals_precentage * .01)
            else:
                occupancy_goals_precentage = 95
            self.income_schema["occupancy_goals_list"].append(round(occupancy_goals_precentage,2))
        
    def loss_gain(self):
        self.income_schema["loss_gain_lease_list"] = []
        for month in range(12):
            loss_gain_lease = self.income_schema["actual_status_timeseries_list"][month] - self.income_schema["gross_rent_potential"][month]
            self.income_schema["loss_gain_lease_list"].append(loss_gain_lease)

    def occupied_vacant_units(self, user_id, property_id):
        amount_units = self.actual_status(user_id, property_id)
        self.income_schema["occuppied_units_list"]  = []
        self.income_schema["vacant_units_list"] = []
        for month in range(12):
            occupied_units = self.income_schema["occupancy_goals_list"][month] * amount_units
            self.income_schema["occuppied_units_list"].append(occupied_units)
            self.income_schema["vacant_units_list"].append(amount_units - occupied_units)
    
    def rent_loss(self,user_id, property_id):
        units_information = self.units_base_info(user_id, property_id)
        self.income_schema["vacancy_loss_list"] = []
        self.income_schema["concessions_list"] = []
        self.income_schema["write_offs_list"] = []

        for month in range(12):
            vacancy_loss = (self.income_schema["actual_status_timeseries_list"][month]/self.income_schema["occuppied_units_list"][month])*self.income_schema["vacant_units_list"][month]
            self.income_schema["vacancy_loss_list"].append(vacancy_loss)
            self.income_schema["concessions_list"].append(self.income_schema["actual_status_timeseries_list"][month] * units_information["concessions"])
            self.income_schema["write_offs_list"].append(self.income_schema["actual_status_timeseries_list"][month] * units_information["write_offs"])