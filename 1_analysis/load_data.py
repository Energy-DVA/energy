import pandas as pd
import geopandas as gpd
from utils import read_prod_data
#%% Read oil prod data
df_oil = read_prod_data("data/oil_lease_production/oil_leases_1980_1989.zip")
df_gas = read_prod_data("data/gas_lease_production/gas_leases_1980_1989.zip")
#%% read lease csv
df_lease = pd.read_csv("data/all_kansas_leases.txt", header=0)
#%% Read fields shapefile
fields = gpd.read_file("data/OILGAS_FIELDS_GEO/OILGAS_FIELDS_GEO.shp")
#%% Read wells csv
df_wells = pd.read_csv("data/ks_wells.txt", header=0, nrows=1000)
#%% Read well tops
df_tops = pd.read_csv("data/ks_tops.txt", header=0, nrows=1000)

