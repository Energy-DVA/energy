from components.data_manager import DataManager

db_path = "/data/kansas_oil_gas.db"
db_type = "sqlite"
dm = DataManager(db_type, db_path)

selected_data = None