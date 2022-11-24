import pandas as pd
import geopandas as gpd
from _1_analysis.utils import read_prod_data
from _1_analysis.db_schema import (
    DROP_LEASE_COLS,
    DROP_WELL_COLS,
    DROP_TOPS_COLS,
    meta,
    OIL_PROD_TABLE,
    GAS_PROD_TABLE,
    LEASE_TABLE,
    WELLS_TABLE,
    TOPS_TABLE,
)
from pathlib import Path
from sqlalchemy import create_engine

#%% Create engine
engine = create_engine("sqlite:///data/kansas_oil_gas.db")
#%% Create tables
meta.create_all(engine)
#%% Path to oil production data folder
oil_path = Path("data/oil_lease_production")
# Path to gas production data folder
gas_path = Path("data/gas_lease_production")
#%% Read and write to sql the oil production data
for file in oil_path.glob("*.zip"):
    df = read_prod_data(file)
    df.to_sql(OIL_PROD_TABLE, engine, if_exists="append", index=False)
#%% Read and write to sql the gs production data
for file in gas_path.glob("*.zip"):
    df = read_prod_data(file)
    df = df.drop_duplicates(["LEASE_KID", "DATE"])
    df.to_sql(GAS_PROD_TABLE, engine, if_exists="append", index=False)
    print(file)
#%% read lease csv
df_lease = pd.read_csv("data/all_kansas_leases.txt", header=0).drop(
    DROP_LEASE_COLS, axis=1
)
df_lease.to_sql(LEASE_TABLE, engine, if_exists="replace", index=False)
#%% Read fields shapefile
# fields = gpd.read_file("data/OILGAS_FIELDS_GEO/OILGAS_FIELDS_GEO.shp")
#%% Read wells csv
df_wells = pd.read_csv("data/ks_wells.txt", header=0).drop(DROP_WELL_COLS, axis=1)
#%% Parse date columns
df_wells["PERMIT"] = pd.to_datetime(df_wells["PERMIT"])
df_wells["SPUD"] = pd.to_datetime(df_wells["SPUD"])
df_wells["COMPLETION"] = pd.to_datetime(df_wells["COMPLETION"])
df_wells["PLUGGING"] = pd.to_datetime(df_wells["PLUGGING"])
df_wells["MODIFIED"] = pd.to_datetime(df_wells["MODIFIED"])
#%% Write to sql
df_wells.to_sql(WELLS_TABLE, engine, if_exists="replace", index=False)
#%% Read well tops
df_tops = pd.read_csv("data/ks_tops.txt", header=0).drop(DROP_TOPS_COLS, axis=1)
#%% Parse dates
df_tops["UPDATED"] = pd.to_datetime(df_tops["UPDATED"])
#%% Find duplicates in tops
dup_tops = df_tops.duplicated(subset=["KID", "FORMATION"], keep=False)
df_dup_tops = df_tops[dup_tops]
df_dup_tops = df_dup_tops.sort_values("UPDATED")
df_dup_last = df_dup_tops.groupby(["KID", "FORMATION"]).last().reset_index()
df_tops_clean = pd.concat([df_tops[~dup_tops], df_dup_last])
#%%
df_tops_clean.to_sql(TOPS_TABLE, engine, if_exists="replace", index=False)
