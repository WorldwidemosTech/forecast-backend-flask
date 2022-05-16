occupancy_goals_precentage = 93
occupancy_goals_list = [occupancy_goals_precentage]
for month in range(11):
    if occupancy_goals_precentage < 94:
        occupancy_goals_precentage += (occupancy_goals_precentage * .01)
    else:
        occupancy_goals_precentage = 95
    occupancy_goals_list.append(round(occupancy_goals_precentage,2))

print(occupancy_goals_list)