from src.config.database import property_information_collection
from src.config.database import property_forecast_collection
from src.utilities.forecast.property_information import Property
from bson import ObjectId

class Income(Property):
    
    def __init__(self, user_id, property_id):
        Property.__init__(self, user_id, property_id)
        self.property_info = property_information_collection
        self.property_forecast = property_forecast_collection
        self.income_schema = {}
        self.income_schema_post = {"income": self.income_schema}

    
    def execute(self):
        self.unit_rents()
        self.actual_status()
        self.occupancy_goals()
        self.loss_gain()
        self.occupied_vacant_units()
        self.rent_loss()
        self.new_leases()
        self.application_fee()
        self.total_rent_income()
        self.big_total_income()
        self.income_schema_post["user_id"] = self.user_id
        self.income_schema_post["property_id"] = self.property_id
        self.property_forecast.insert_one(self.income_schema_post)
        return self.income_schema_post

    def unit_rents(self):
        total_rent = Property.units_info(self)
        average_monthly_increase_grp = (sum(total_rent["new_rent"]) - sum(total_rent["actual_rent"]))/12
        gross_rent_potential = sum(total_rent["actual_rent"]) + average_monthly_increase_grp
        
        self.income_schema["gross_rent_potential"] = [round(gross_rent_potential)]
        for month in range(11):
            self.income_schema["gross_rent_potential"].append(round(average_monthly_increase_grp + self.income_schema["gross_rent_potential"][month]))
        
    def actual_status(self):
        units_information = Property.units_base_info(self)
        total_rent = Property.units_info(self)
        amount_units = sum(total_rent["total_units"])
        turnover = units_information["turnover"]
        monthly_moveouts = round(amount_units * turnover/12)
        actual_status = (units_information["actual_income"]/(amount_units - sum(total_rent["vacant_units"]))) * amount_units
        current_loss_to_lease = -(sum(total_rent["actual_rent"])-actual_status)
        current_actual_rent = sum(total_rent["actual_rent"]) + current_loss_to_lease
        per_unit_rent_growth_market = (sum(total_rent["new_rent"]) - current_actual_rent) / amount_units
        per_unit_rent_growth_renewal = (sum(total_rent["actual_rent"]) * .02) / amount_units
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

    def occupancy_goals(self):
        
        amount_units = self.actual_status()
        total_rent = Property.units_info(self)
        occupancy_goals_precentage = ((amount_units - sum(total_rent["vacant_units"]))/amount_units)*100

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

    def occupied_vacant_units(self):
        amount_units = self.actual_status()
        self.income_schema["occuppied_units_list"]  = []
        self.income_schema["vacant_units_list"] = []
        for month in range(12):
            occupied_units = self.income_schema["occupancy_goals_list"][month]/100 * amount_units
            self.income_schema["occuppied_units_list"].append(round(occupied_units))
            self.income_schema["vacant_units_list"].append(round(amount_units - occupied_units))
    
    def rent_loss(self):
        units_information = Property.units_base_info(self)
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
 
    def application_fee(self):
        units_information = Property.units_base_info(self)
        self.income_schema["application_fees"] = []

        for month in range(12):
            self.income_schema["application_fees"].append(self.income_schema["new_leases"][month]*2*units_information["application_fee"])

    def total_rent_income(self):
        self.income_schema["total_rental_income"] = []
        for month in range(12):
            value_1 = self.income_schema["actual_status_timeseries_list"][month]
            value_2 = self.income_schema["vacancy_loss_list"][month]
            value_3 = self.income_schema["concessions_list"][month]
            value_4 = self.income_schema["write_offs_list"][month]
            total_sum = (value_1 + value_2 + value_3 + value_4)
            self.income_schema["total_rental_income"].append(total_sum)
    
    def big_total_income(self):
        document = self.property_info.find_one({"user_id":self.user_id, "property_id":ObjectId(self.property_id)})
        self.income_schema["big_total_income"] = []
        income_document = document["income"].values()
        income_entered_by_user = sum([i for i in income_document ])

        for income_concepts in document["income"]:
             self.income_schema[income_concepts] = document["income"][income_concepts]

        for month in range(12):
            self.income_schema["big_total_income"].append(self.income_schema["total_rental_income"][month] + self.income_schema["application_fees"][month] + income_entered_by_user)
        

'''def main():
    income = Income("dlopezvsr", "62e851b0c710e7c50f913e14")
    print(income.execute())

if __name__ == "__main__":
    main()'''