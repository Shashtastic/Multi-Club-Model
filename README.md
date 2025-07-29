# Multi-Club-Model
This repository contains a comprehensive Monte Carlo simulation model to evaluate the valuation of mid and lower-tier football clubs in Europe. The model integrates sporting, financial, and branding indicators to simulate a club’s estimated worth in million Euros, tailored for nuanced European football ecosystems.

# Core Components
1. Brand Value:
    1. Local following: Attendance rate, city size, club competition.
       
    2. Global following: Social media followers, Google Trends, international exposure.
       
    3. Geographical context: City economic index, expat representation, and city-specific multipliers.

2. Sporting Potential:
   1. Youth player emergence probability based on city size and competition.

   2. Outgoing transfer potential via lognormal distributions.

   3. Adjustments for stadium size, managerial and league stability.

3. Financial Health:
   1. Payroll-to-income ratio multipliers.
     
   2. Profitability multipliers (normalised between historical bounds).
     
   3. Revenue scale via log-normal transformations
     
   4. Adjustments for stadium ownership, shared usage, European competition and relegation qualification.
     
   5. Country-specific relegation sensitivity.
  

# Dependencies
1. Python
2. Numpy
3. Pandas
4. Matplotlib
5. Openyxl

This is to verIfy that Shashwat Gupta, B.A. (H) Economics student from Hindu College has made this.
