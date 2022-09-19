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

#%% Create the oil_production table
meta = MetaData()
oil_production = Table(
    "oil_production",
    meta,
    Column("LEASE_KID", Integer, primary_key=True),
    Column("DATE", Date, primary_key=True),
    Column("WELLS", Integer),
    Column("PRODUCTION", Float),
)
#%% Create the gas_production table
gas_production = Table(
    "gas_production",
    meta,
    Column("LEASE_KID", Integer, primary_key=True),
    Column("DATE", Date, primary_key=True),
    Column("WELLS", Integer),
    Column("PRODUCTION", Float),
)
#%% Create the lease table
lease = Table(
    "lease",
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
#%% Create engine
engine = create_engine("sqlite:///data/kansas_oil_gas.db")
