import pandas as pd
from components.data_manager import DataManager
from components.forecaster import Forecaster
import matplotlib.pyplot as plt

#%% Create data manager
db_path = "/data/kansas_oil_gas.db"
db_type = "sqlite"
dm = DataManager(db_type, db_path)
#%% Get all production data
# df_lease = dm.get_lease_info()
# lease_ids = df_lease[dm.L_LEASE_ID].tolist()
df_prod = dm.get_production_from_ids("oil", years_range=(1930, 2020))
pred_period = 36
#%% Create forecaster for SARIMA
sarima = Forecaster(df_prod[dm.CV_P_CAL_DAY_PROD])
df_sarima_res = sarima.fit_predict(pred_period)
#%% Plot results
df_sarima_res.plot()
plt.show()
#%% Create forecaster for sarimax
n_wells = 18000
wells_arr = pd.DataFrame([n_wells] * pred_period)
#%%
sarimax = Forecaster(df_prod[dm.CV_P_CAL_DAY_PROD], df_prod[[dm.P_WELLS]])
df_sarimax_res = sarimax.fit_predict(pred_period, wells_arr)
#%% predict
df_sarimax_res = sarimax.predict(pred_period, wells_arr)
#%% Plot results
df_sarimax_res.plot()
plt.show()
