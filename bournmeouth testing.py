import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

num_simulations = 10000

#BRAND VALUE

# LOCAL FOLLOWING 

    # Population
population = 200
population_multiplier = np.full(num_simulations, (np.log(population*1000) - np.log(80*1000)) / (np.log(10000*1000) - np.log(80*1000))) # np.log15000 is taken for europe, np.log50000 is taken for worldwide

    # Past performance
mu_perf = 44.3
sigma_perf = 7
performance = np.random.normal(loc=mu_perf, scale=sigma_perf, size=num_simulations)

    # Thresholds
ucl_perf = 68.6
europa_perf = 62.2
relegation_perf = 31.8

   # Attendance rate (bounded between 0 and 1) — higher means better sentiment
attendance = 0.91 # e.g., 0.96 for 96% attendance

def adjusted_attendance_count (performance, relegation_perf, europa_perf, ucl_perf):
    attendance_ucl_adjustment = np.where(performance > ucl_perf, 1.068, 1)   #60
    attendance_europpa_adjustment = np.where(performance > europa_perf, 1.035, 1)   #53
    attendance_relegation_adjustment = np.where(performance < relegation_perf, 0.935, 1)   #28.5
    adjusted_attendance_inside = (
        attendance * 
        attendance_ucl_adjustment * 
        attendance_europpa_adjustment * 
        attendance_relegation_adjustment
        )
    return adjusted_attendance_inside

adjusted_attendance = attendance * adjusted_attendance_count (performance, relegation_perf, europa_perf, ucl_perf)

# Addendum to adjusted attendance
other_clubs_in_region = 1
if other_clubs_in_region <= 2:
    if np.mean(adjusted_attendance) <= 0.9:
        club_adjusted_attendance = adjusted_attendance * 1.033
    else: 
        club_adjusted_attendance = adjusted_attendance * 1.02
elif other_clubs_in_region < 3:
    if np.mean(adjusted_attendance) <= 0.9:
        club_adjusted_attendance = adjusted_attendance * 1.02
    else:
        club_adjusted_attendance = adjusted_attendance * 1.01
else:
   club_adjusted_attendance = adjusted_attendance * 1
club_adjusted_attendance = np.clip(club_adjusted_attendance, 0, 0.999)
    
 # GLOBAL FOLLOWING   
    # Social media follower score (counts of mentions/posts)
total_social_media_followers = 1500 # e.g., 787 for 787k followers

def adjusted_follower_count(performance, relegation_perf, europa_perf, ucl_perf):
    follower_adjustment = np.zeros_like(performance)
    follower_adjustment += np.where(performance < relegation_perf, total_social_media_followers * -0.018, 0.01)
    follower_adjustment += np.where(performance > europa_perf, total_social_media_followers * 0.05, 0.01)
    follower_adjustment += np.where(performance > ucl_perf, total_social_media_followers * 0.1, 0.01)
    adjusted_followers_inside = total_social_media_followers + (1 * follower_adjustment)

    return adjusted_followers_inside

adjusted_followers = adjusted_follower_count(performance, relegation_perf, europa_perf, ucl_perf)

    # Google trends average over past 5 years
g_trends_average = 12.3


# GEOGRAPHICAL CONSIDERATIONS
    # City economic prosperity index (e.g., GDP per capita, scaled index between 0 and 1)
city_gdp_per_capita_usd = 42900  # e.g., 15000 per person

    # Country of club expats in top 5 leagues factor
df = pd.read_excel("/Users/shashwatgupta/Desktop/Started/CountryBV.xlsx")

df['Country'] = df['Country'].str.strip().str.lower()

country_input = input("Enter a country name: ").strip().lower()

match = df[df['Country'] == country_input]

if not match.empty:
    country_bv_mp = match['country_bv_mp'].values[0]
    print(f"The associated number for {country_input.title()} is: {country_bv_mp} ")
else:
    print("Country not found in the Excel file.")

    # City multiplier
df = pd.read_excel("/Users/shashwatgupta/Desktop/Started/cities.xlsx")

df['City'] = df['City'].str.strip().str.lower()

city_input = input("Enter a city name: ").strip().lower()

match = df[df['City'] == city_input]

if not match.empty:
    city_score = match['CityScore'].values[0]
    print(f"The associated number for {city_input.title()} is: {city_score}")
else:
    city_score = 1
    print("City not found in the Excel file.")


    # Normalize variables to 0–1 scale
local_norm = (club_adjusted_attendance - np.min(adjusted_attendance)) / (1 - np.min(adjusted_attendance)) # Local Following Norm Construction
g_trends_norm = np.full(num_simulations, (np.log(g_trends_average) - np.log(1)) / (np.log(12) - np.log(1))) #log12 is taken because we are not taking popular clubs into account
follower_norm = np.full(num_simulations, (np.log(adjusted_followers*1000) - np.log(50*1000)) / (np.log(1000*1000) - np.log(50*1000)))
city_gdp_norm = np.full(num_simulations, (np.log(city_gdp_per_capita_usd) - np.log(500)) / (np.log(72000) - np.log(500)))

    # Local Following Norm Construction
local_norm = local_norm * city_score 

    # Global Following Norm Construction
global_norm = (0.35 * g_trends_norm) + (0.65 * follower_norm)

    # Geography Norm construction
geo_norm = city_gdp_norm + (country_bv_mp * city_score)
geography_norm = np.full(num_simulations, (geo_norm - 0.1) / (1.9))

# Brand Index
brand_index = (
    0.50 * local_norm +
    0.25 * global_norm  +
    0.25 * geography_norm
)


#SPORTING POTENTIAL
    # Country of club expats in top 5 leagues factor

df = pd.read_excel("/Users/shashwatgupta/Desktop/Started/countries.xlsx")

df['Country'] = df['Country'].str.strip().str.lower()

match = df[df['Country'] == country_input]

if not match.empty:
    score = match['Score'].values[0]
    print(f"The associated number for {country_input.title()} is: {score}")
else:
    print("Country not found in the Excel file.")

# PLAYER SALE

        #Chance of youth player emergence
def youth_emergence_probability(other_clubs_in_region, population_multiplier):

    if other_clubs_in_region > 3:
        p_emerge_base = 0.059
    else:
        p_emerge_base = 0.09

    p_emerge_variable = p_emerge_base 
    p_emerge_inside = np.mean(p_emerge_variable)

    return p_emerge_inside

p_emerge = youth_emergence_probability(other_clubs_in_region, population_multiplier)

        #Transfer fees outside youth sales
transfer_outgoing = 17.2

def transfers_outgoing():
    if transfer_outgoing > 10:
        mean_ln_in, sigma_ln_in = 3.5, 0.5
    elif transfer_outgoing > 5:
        mean_ln_in, sigma_ln_in = 2.6, 0.5
    elif transfer_outgoing > 3:
        mean_ln_in, sigma_ln_in = 2.4, 0.5
    elif transfer_outgoing > 1:
        mean_ln_in, sigma_ln_in = 2.2, 0.5
    elif transfer_outgoing > 0.4:
        mean_ln_in, sigma_ln_in = 2.0, 0.5
    else:
        mean_ln_in, sigma_ln_in = 1.8, 0.5

    return mean_ln_in, sigma_ln_in

mean_ln, sigma_ln = transfers_outgoing()

    # Simulation
def simulate_academy_product():

    emerges = np.random.binomial(n=130, p=p_emerge)

    if emerges:
        value = np.random.lognormal(mean=mean_ln, sigma=sigma_ln)
    else:
        value = 0

    return value

simulated_values = np.array([simulate_academy_product() for _ in range(num_simulations)])

net_values = simulated_values + transfer_outgoing

if np.max(net_values) == np.min(net_values):
    net_values_norm = np.zeros(num_simulations)
else:
    net_values_norm = (np.log(net_values) - np.log(np.min(net_values))) / np.log((np.max(net_values)) - np.log(np.min(net_values)))

# STADIUM CAPACITY
capacity = 12000

def stadium_cap_weight():
    thresholds = [
        (10000, 0.45), (12500, 0.5), (15000, 0.55), (17500, 0.6), (20000, 0.65),
        (22500, 0.7), (25000, 0.75), (27500, 0.8), (30000, 0.85),
        (33333, 0.9), (36666, 0.95), (40000, 1.0)
    ]
    for t, w in thresholds:
        if capacity <=t:
            return w
    else: return 1.5

stadium_capacity_weight = stadium_cap_weight()

# LEAGUE STABILITY
league_stability = 3.2
if league_stability < 3:
    league_stability_multiplier = 1.2
elif league_stability < 4:
    league_stability_multiplier = 1.13
elif league_stability < 5:
    league_stability_multiplier = 1.06
else:
    league_stability_multiplier = 1

# MANAGER STABILITY
no_managers = 3

avg_tenure = 3/no_managers
def manager_stability():
    if avg_tenure > 2.99:
        man_stability_multiplier = 1.3
    elif avg_tenure > 1.49:
        man_stability_multiplier = 1
    elif avg_tenure > 0.99:
        man_stability_multiplier = 0.85
    elif avg_tenure > 0.749:
        man_stability_multiplier = 0.68
    else:
        man_stability_multiplier = 0.60
    
    return man_stability_multiplier

manager_stability_multiplier = manager_stability()

# Weights
net_values_weight = 0.64
score_weight = 0.25
adjusted_stad_cap_weight = 0.05
manager_stability_multiplier_weight = 0.15

# Sporting Potential Score
sporting_norm= (
    ((net_values_norm * net_values_weight) + 
     (score * score_weight) + 
     (adjusted_stad_cap_weight * stadium_capacity_weight) +
     (manager_stability_multiplier_weight * manager_stability_multiplier)) * 
     league_stability_multiplier
     )

# FINANCIAL VALUE

    # Non-Transfer Revenue
operating_income = 169500
payroll = 130170
profit_before_tax = -19601
max_profit_before_tax = 44000
min_profit_before_tax = -55123
profit_before_tax_norm = ((profit_before_tax - min_profit_before_tax)/ (max_profit_before_tax - min_profit_before_tax))

def wage_to_income_ratio ():
    wage_income_ratio_inside = payroll/operating_income
    if wage_income_ratio_inside < 0.5:
        wir_multiplier = 2.5
    elif wage_income_ratio_inside < 0.6:
        wir_multiplier = 2.2
    elif wage_income_ratio_inside < 0.7:
        wir_multiplier = 2.0
    elif wage_income_ratio_inside < 0.8:
        wir_multiplier = 1.7
    elif wage_income_ratio_inside < 0.9:
        wir_multiplier = 1.4
    elif wage_income_ratio_inside < 1.0:
        wir_multiplier = 1.
    elif wage_income_ratio_inside < 1.1:
        wir_multiplier = 0.85
    else:
        wir_multiplier = 0.68

    return wir_multiplier

wage_to_income_ratio_multiplier = wage_to_income_ratio ()

def profit_multiple ():
    if profit_before_tax_norm < 0.375:
        profit_multiplier = 0.6
    elif profit_before_tax_norm < 0.43:
        profit_multiplier = 0.7
    elif profit_before_tax_norm < 0.5:
        profit_multiplier = 0.8
    elif profit_before_tax < 0.6:
        profit_multiplier = 1
    elif profit_before_tax_norm < 0.7:
        profit_multiplier = 1.15
    elif profit_before_tax_norm < 0.8:
        profit_multiplier = 1.3
    elif profit_before_tax_norm < 0.85:
        profit_multiplier = 1.4
    else:
        profit_multiplier = 1.475

    return profit_multiplier

profitability_multiplier = profit_multiple ()

def sales():
    sales_norm = ((np.log(operating_income * 1000) - np.log(5000*1000))/(np.log(55000*1000) - np.log(5000*1000)))
    return sales_norm

sales_multiplier = sales()

financial_multiplier = (0.23 * wage_to_income_ratio_multiplier) + (0.10 * profitability_multiplier) + (0.67 *sales_multiplier)


#Weights
brand_index_weight = 0.23
sporting_norm_weight = 0.33
financial_multiplier_weight = 0.44

Value_Index = (
    (brand_index_weight * (brand_index)) + 
    (sporting_norm_weight * (sporting_norm)) + 
    (financial_multiplier_weight * financial_multiplier)
    )

#English Multiplier 

if country_input == "england":
    print ()
    english_club_type = input("What type of Club: Premier League Club (1), Relegated Premier League Club(2), Championship Club(3), L1/L2 Club(4) \x1B[3m (Write corresponding number)\x1B[0m: ")
    if english_club_type == "1":
        english_multiplier = 1.8
    elif english_club_type == "2":
        english_multiplier = 1.6
    elif english_club_type == "3":
        english_multiplier = 1.45
    elif english_club_type == "4":
        english_multiplier = 1.35
    else:
        english_multiplier = 1

    club_valuations = Value_Index*100* english_multiplier
else:
    club_valuations = Value_Index*100

#OUTPUT
plt.figure(figsize=(10, 6))
plt.hist(club_valuations, bins=50, color='skyblue', edgecolor='black')
plt.title('Monte Carlo Simulation of Football Club Valuation')
plt.xlabel('Valuation (in million $)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

print (f"Median Club Valuation: {np.median(club_valuations):,.5f}")
print (f"Mean Club Valuation: {np.mean(club_valuations):,.5f}")
print (f"Value Index: {np.mean(Value_Index):,.5f}")
print (f"Fincial Multiplier: {np.mean(financial_multiplier):,.5f}")
print (f"Brand Index: {np.mean(brand_index):,.5f}")
print (f"Sporting Potential Score: {np.mean(sporting_norm):,.5f}")