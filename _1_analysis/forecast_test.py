from src.pages.forecast.data_manager import DataManager
#%% Create data manager
db_path = "/data/kansas_oil_gas.db"
db_type = "sqlite"
dm = DataManager(db_type, db_path)
#%% Get all production data
df_prod = dm.get_production_from_ids("gas")
