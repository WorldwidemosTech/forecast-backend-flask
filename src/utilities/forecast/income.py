from re import M
from src.config.database import property_information_collection
from src.config.database import property_forecast_collection

class Income():
    
    def __init__(self):
        self.property_info = property_information_collection
        self.property_forecast = property_forecast_collection
        self.income_schema = {}
    
    def execute(self, user_id, property_id):
        self.units_base_info(user_id, property_id)
        self.units_info(user_id, property_id)
        self.unit_rents(user_id, property_id)
        self.actual_status(user_id, property_id)
        self.occupancy_goals(user_id, property_id)
        self.loss_gain()
        self.occupied_vacant_units(user_id, property_id)
        self.rent_loss(user_id, property_id)
        self.new_leases()
        self.application_fee(user_id, property_id)
        self.total_rent_income(user_id, property_id)
        self.big_total_income(user_id, property_id)
        self.income_schema["user_id"] = user_id
        self.income_schema["property_id"] = property_id
        response = self.property_forecast.insert_one(self.income_schema)
        return self.income_schema

    def units_base_info(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        units_information = document["property_information"]
        return units_information
    
    def units_info(self, user_id, property_id):
        units_information = self.units_base_info(user_id, property_id)
        total_rent = {"actual": [], "new": [], "vacant": [], "total_units":[]}

        for rent in units_information["units_information"]:
            actual = rent["amount_units"] * rent["actual_month_rent"]
            new = rent["amount_units"] * rent["new_month_rent"]
            total_rent["actual"].append(actual)
            total_rent["new"].append(new)
            total_rent["vacant"].append(rent["vacant"])
            total_rent["total_units"].append(rent["amount_units"])
        return total_rent

    def unit_rents(self, user_id, property_id):
        total_rent = self.units_info(user_id, property_id)
        average_monthly_increase_grp = (sum(total_rent["new"]) - sum(total_rent["actual"]))/12
        gross_rent_potential = sum(total_rent["actual"]) + average_monthly_increase_grp
        
        self.income_schema["gross_rent_potential"] = [round(gross_rent_potential)]
        for month in range(11):
            self.income_schema["gross_rent_potential"].append(round(average_monthly_increase_grp + self.income_schema["gross_rent_potential"][month]))
        
    def actual_status(self, user_id, property_id):
        units_information = self.units_base_info(user_id, property_id)
        total_rent = self.units_info(user_id, property_id)
        amount_units = sum(total_rent["total_units"])
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

        self.income_schema["monthly_moveouts"] = [monthly_moveouts]
        self.income_schema["actual_status_timeseries_list"] = [round(actual_status_timeseries)]
        for month in range(11):
            self.income_schema["actual_status_timeseries_list"].append(round(self.income_schema["actual_status_timeseries_list"][month]+ average_monthly_increase_actual))

        return amount_units

    def occupancy_goals(self, user_id, property_id):
        
        amount_units = self.actual_status(user_id, property_id)
        total_rent = self.units_info(user_id, property_id)
        occupancy_goals_precentage = ((amount_units - sum(total_rent["vacant"]))/amount_units)*100

        self.income_schema["occupancy_goals_list"] = [round(occupancy_goals_precentage)]

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
            occupied_units = self.income_schema["occupancy_goals_list"][month]/100 * amount_units
            self.income_schema["occuppied_units_list"].append(round(occupied_units))
            self.income_schema["vacant_units_list"].append(round(amount_units - occupied_units))
    
    def rent_loss(self,user_id, property_id):
        units_information = self.units_base_info(user_id, property_id)
        self.income_schema["vacancy_loss_list"] = []
        self.income_schema["concessions_list"] = []
        self.income_schema["write_offs_list"] = []

        for month in range(12):
            # Negative values
            vacancy_loss = (self.income_schema["actual_status_timeseries_list"][month]/self.income_schema["occuppied_units_list"][month])*self.income_schema["vacant_units_list"][month]
            self.income_schema["vacancy_loss_list"].append(round(-vacancy_loss))
            self.income_schema["concessions_list"].append(round(-(self.income_schema["actual_status_timeseries_list"][month] * units_information["concessions"])))
            self.income_schema["write_offs_list"].append(round(-(self.income_schema["actual_status_timeseries_list"][month] * units_information["write_offs"])))

    def new_leases(self):
        self.income_schema["new_leases"] = [0]
        
        for month in range(11):
            new_lease = self.income_schema["vacant_units_list"][month] + self.income_schema["monthly_moveouts"][0] - self.income_schema["vacant_units_list"][month+1]
            self.income_schema["new_leases"].append(new_lease)
 
    def application_fee(self, user_id, property_id):
        units_information = self.units_base_info(user_id, property_id)
        self.income_schema["application_fees"] = []
        self.income_schema["new_leases"]

        for month in range(12):
            self.income_schema["application_fees"].append(self.income_schema["new_leases"][month]*2*units_information["application_fee"])

    def total_rent_income(self, user_id, property_id):
        self.income_schema["total_rental_income"] = []
        units_information = self.units_base_info(user_id, property_id)
        for month in range(12):
            value_1 = self.income_schema["actual_status_timeseries_list"][month]
            value_2 = self.income_schema["vacancy_loss_list"][month]
            value_3 = self.income_schema["concessions_list"][month]
            value_4 = self.income_schema["write_offs_list"][month]
            total_sum = (value_1 + value_2 + value_3 + value_4)
            self.income_schema["total_rental_income"].append(total_sum)
    
    def big_total_income(self, user_id, property_id):
        document = self.property_info.find_one({"user_id":user_id, "property_id":property_id})
        self.income_schema["big_total_income"] = []
        income_document = document["income"].values()
        income_entered_by_user = sum([i for i in income_document ])

        for income_concepts in document["income"]:
             self.income_schema[income_concepts] = document["income"][income_concepts]

        for month in range(12):
            self.income_schema["big_total_income"].append(self.income_schema["total_rental_income"][month] + income_entered_by_user)
        

def main():
    income = Income()
    print(income.execute("dlopezvsr", "6223cf8c40b07aaf6c4f36b1"))

if __name__ == "__main__":
    main()