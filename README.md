# CyclingTrafficInParis
Google Sheet for Data Audit: https://docs.google.com/spreadsheets/d/1JBR-bky2OLdFRM9l6IupNMDDhdjEt1Wd1ybVp14ltNk/edit?usp=sharing

Updated Data Audit sheet: https://tinyurl.com/4sb7m9xb)](https://tinyurl.com/4sb7m9xb (Status: 06.12.2023 - 16:40)

Overview upon machine learning models: https://docs.google.com/spreadsheets/d/1xR9cTEGTaXCzOJSIsBJ3SBywne_-Ueqn3FDRwAW8xA0

Dataset page: https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/information

The dataset contains hourly counts of bicycles in Paris from the last 13 months. The counters are installed on bicycle lanes and some bus lanes.
The CSV.zip contains all but the initial ZIP files and enables to run all scripts for visualisation or machine learning.

The nov23_bda_int_cycling_in_paris.zip contains all Python scripts that were used in the pipeline as well as all datasources (.csv files). The split datasets for machine learning exist in two variant (e.g. X_train.csv and X_train_weather.csv). Files with weather include weather data, while the other files just contain the bicycle counts including holiday information.