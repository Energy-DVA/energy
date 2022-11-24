from sqlalchemy import create_engine, MetaData
from sqlalchemy import select, func
from _1_analysis.db_schema import OIL_PROD_TABLE, LEASE_TABLE
import pandas as pd
import matplotlib.pyplot as plt

#%% Create engine
engine = create_engine("sqlite:///data/kansas_oil_gas.db")
#%% Reflect oil production table
meta = MetaData()
meta.reflect(bind=engine)
oil_prod = meta.tables[OIL_PROD_TABLE]
#%% Group by date and sum the WELLS and PRODUCTION columns using sqlalchemy
s = select(
    [
        oil_prod.c.DATE,
        func.sum(oil_prod.c.WELLS).label("N_WELLS"),
        func.sum(oil_prod.c.PRODUCTION).label("MONTHLY_OIL_PROD"),
    ]
).group_by(oil_prod.c.DATE)

#%% Execute query
df_oil_prod = pd.read_sql(s, engine)
#%% Parse date column and set as index and order it
df_oil_prod["DATE"] = pd.to_datetime(df_oil_prod["DATE"])
#%% Calculate the number of days in each month
df_oil_prod["N_DAYS"] = df_oil_prod["DATE"].dt.daysinmonth
#%% Set date as index
df_oil_prod = df_oil_prod.set_index("DATE").sort_index()
#%% Calculate the calendar day production
df_oil_prod["CAL_DAY_PROD"] = df_oil_prod["MONTHLY_OIL_PROD"] / df_oil_prod["N_DAYS"]
#%% Plot the calendar day production
df_oil_prod.plot(y="CAL_DAY_PROD", figsize=(12, 8))
plt.show()
