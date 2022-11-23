from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    Float,
    Date,
)
from sqlalchemy import create_engine

#%% Table names
OIL_PROD_TABLE = "oil_production"
GAS_PROD_TABLE = "gas_production"
LEASE_TABLE = "lease"
WELLS_TABLE = "wells"
TOPS_TABLE = "tops"
#%% Specify columns to drop from the data sources
DROP_PROD_COLS = [
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

DROP_LEASE_COLS = [
    "TOWNSHIP",
    "TWN_DIR",
    "RANGE",
    "RANGE_DIR",
    "SECTION",
    "SPOT",
]

DROP_WELL_COLS = [
    "TOWNSHIP",
    "TWN_DIR",
    "RANGE",
    "RANGE_DIR",
    "SECTION",
    "SPOT",
    "FEET_NORTH",
    "FEET_EAST",
    "FOOT_REF",
    "IP_OIL",
    "IP_GAS",
    "IP_WATER",
    "OIL_KID",
    "OIL_DOR_ID",
    "GAS_KID",
    "GAS_DOR_ID",
    "KCC_PERMIT",
]

DROP_TOPS_COLS = [
    "API_NUMBER",
    "API_NUM_NODASH",
    "ELEVATION",
    "ELEV_REF",
]
#%% Create the oil_production table
meta = MetaData()
oil_production = Table(
    OIL_PROD_TABLE,
    meta,
    Column("LEASE_KID", Integer, primary_key=True),
    Column("DATE", Date, primary_key=True),
    Column("WELLS", Integer),
    Column("PRODUCTION", Float),
)
#%% Create the gas_production table
gas_production = Table(
    GAS_PROD_TABLE,
    meta,
    Column("LEASE_KID", Integer, primary_key=True),
    Column("DATE", Date, primary_key=True),
    Column("WELLS", Integer),
    Column("PRODUCTION", Float),
)
#%% Create the lease table
lease = Table(
    LEASE_TABLE,
    meta,
    Column("LEASE_KID", Integer, primary_key=True),
    Column("LEASE", String),
    Column("DOR_CODE", Integer),
    Column("API_NUMBER", String),
    Column("OPERATOR", String),
    Column("COUNTY", String),
    Column("LATITUDE", Float),
    Column("LONGITUDE", Float),
    Column("PRODUCES", String),
    Column("PRODUCTION", Float),
    Column("YEAR_START", Integer),
    Column("YEAR_STOP", Integer),
    Column("URL", String),
)
#%% Create wells table
wells = Table(
    WELLS_TABLE,
    meta,
    Column("KID", Integer, primary_key=True),
    Column("API_NUMBER", String),
    Column("API_NUM_NODASH", String),
    Column("LEASE", String),
    Column("WELL", String),
    Column("FIELD", String),
    Column("LATITUDE", Float),
    Column("LONGITUDE", Float),
    Column("LONG_LAT_SOURCE", String),
    Column("ORIG_OPERATOR", String),
    Column("CURR_OPERATOR", String),
    Column("ELEVATION", Float),
    Column("ELEV_REF", String),
    Column("DEPTH", Float),
    Column("FORMATION_AT_TOTAL_DEPTH", String),
    Column("PRODUCE_FORM", String),
    Column("PERMIT", Date),
    Column("SPUD", Date),
    Column("COMPLETION", Date),
    Column("PLUGGING", Date),
    Column("MODIFIED", Date),
    Column("STATUS", String),
    Column("STATUS2", String),
    Column("COMMENTS", String),
)
#%% Create tops table
tops = Table(
    TOPS_TABLE,
    meta,
    Column("KID", Integer, primary_key=True),
    Column("FORMATION", String, primary_key=True),
    Column("LONGITUDE", Float),
    Column("LATITUDE", Float),
    Column("TOP", Float),
    Column("BASE", Float),
    Column("SOURCE", String),
    Column("UPDATED", Date),
    Column("OLD_FORMATION", String),
)
