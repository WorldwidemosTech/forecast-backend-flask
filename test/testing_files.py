gross_rent_potential = 11
grp_time_series = [gross_rent_potential]

for value in range(11):
    grp_time_series.append(gross_rent_potential + grp_time_series[value])


montlhy_moveouts = round(300 * 14.5/12)

print(float(montlhy_moveouts*12))