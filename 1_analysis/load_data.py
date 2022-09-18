import pandas as pd
import geopandas as gpd
from utils import preprocess_prod
#%% unzip data and load csv to dataframe
drop_cols = [
    "LEASE",
    "DOR_CODE",
    "API_NUMBER",
    "FIELD",
    "PRODUCING_ZONE",
    "OPERATOR",
    "COUNTY",
    "TOWNSHIP",
    "TWN_DIR",
    "RANGE",
    "RANGE_DIR",
    "SECTION",
    "SPOT",
    "LATITUDE",
    "LONGITUDE",
    "PRODUCT",
    "URL",
]
df = pd.read_csv(
    "data/oil_lease_production/oil_leases_1980_1989.zip",
    compression="zip",
    header=0,
    parse_dates={"DATE": ["MONTH-YEAR"]},
    # nrows=1000,
).drop(drop_cols, axis=1)
#%% Select dates starting with 0
df_oil_prod = preprocess_prod(df, "DATE", "PRODUCTION")
#%% read lease csv
df_lease = pd.read_csv("data/all_kansas_leases.txt", header=0)
#%% Read fields shapefile
fields = gpd.read_file("data/OILGAS_FIELDS_GEO/OILGAS_FIELDS_GEO.shp")
