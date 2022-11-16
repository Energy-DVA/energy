from sqlalchemy import create_engine, select, func, MetaData, and_
from typing import List, Tuple, Optional
import pandas as pd


class DataManager:

    OIL_PROD_TABLE = "oil_production"
    GAS_PROD_TABLE = "gas_production"
    LEASE_TABLE = "lease"
    WELLS_TABLE = "wells"
    TOPS_TABLE = "tops"
    # -- Lease table columns
    L_LEASE_ID = "LEASE_KID"
    L_LEASE_NAME = "LEASE"
    L_OPERATOR = "OPERATOR"
    L_COUNTY = "COUNTY"
    L_LATITUDE = "LATITUDE"
    L_LONGITUDE = "LONGITUDE"
    L_PRODUCES = "PRODUCES"
    # -- Typical PRODUCES Values
    L_PRODUCES_OIL = "OIL"
    L_PRODUCES_GAS = "GAS"
    L_YEAR_START = "YEAR_START"
    L_YEAR_STOP = "YEAR_STOP"
    # -- Production tables (same for both oil and gas)
    P_LEASE_ID = "LEASE_KID"
    P_DATE = "DATE"
    P_WELLS = "WELLS"
    P_PRODUCTION = "PRODUCTION"
    CV_P_CAL_DAY_PROD = "CAL_DAY_PROD"

    def __init__(self, db_type: str, path: str):
        self.db_type = db_type
        self.path = path
        self.engine = create_engine(f"{db_type}://{path}")
        # Reflect tables
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        self.oil_prod = self.meta.tables[self.OIL_PROD_TABLE]
        self.gas_prod = self.meta.tables[self.GAS_PROD_TABLE]
        self.lease = self.meta.tables[self.LEASE_TABLE]
        self.wells = self.meta.tables[self.WELLS_TABLE]
        self.tops = self.meta.tables[self.TOPS_TABLE]

    def _create_conditions(
        self,
        lease_ids: Optional[List[str]],
        counties: Optional[List[str]],
        operators: Optional[List[str]],
        produces: Optional[List[str]],
        years_range: Optional[Tuple[int, int]],
    ):
        conditions = []
        # -- Add lease ids
        if lease_ids is not None:
            conditions.append(self.lease.c[self.L_LEASE_ID].in_(lease_ids))
        # -- Add counties
        if counties is not None:
            conditions.append(self.lease.c[self.L_COUNTY].in_(counties))
        # -- Add operators
        if operators is not None:
            conditions.append(self.lease.c[self.L_OPERATOR].in_(operators))
        # -- Add produces
        if produces is not None:
            conditions.append(self.lease.c[self.L_PRODUCES].in_(produces))
        # -- Add years start
        if years_range is not None:
            conditions.append(
                and_(
                    self.lease.c[self.L_YEAR_START] >= years_range[0],
                    self.lease.c[self.L_YEAR_STOP] <= years_range[1],
                )
            )

        return conditions

    def get_lease_info(
        self,
        cols: Optional[List[str]] = None,
        lease_ids: Optional[List[str]] = None,
        counties: Optional[List[str]] = None,
        operators: Optional[List[str]] = None,
        produces: Optional[List[str]] = None,
        years_start: Optional[List[int]] = None,
    ) -> pd.DataFrame:
        """Get lease info for a list of lease ids, counties and operators"""
        # -- Get the columns to select
        if cols is None:
            s_cols = self.lease
        else:
            s_cols = [self.lease.c[col] for col in cols]

        # -- Create the conditions
        conditions = self._create_conditions(
            lease_ids, counties, operators, produces, years_start
        )

        if len(conditions) >= 1:
            s = select(s_cols).where(and_(*conditions))
        else:
            s = select(s_cols)

        df = pd.read_sql(s, self.engine)

        return df

    def get_production_from_ids(
        self,
        prod_type: str,
        lease_ids: Optional[List[str]] = None,
        agg="sum",
        get_rate=True,
    ):
        """Get production for a list of lease ids"""
        # -- Get the table to query
        if prod_type == "oil":
            table = self.oil_prod
        elif prod_type == "gas":
            table = self.gas_prod
        else:
            raise ValueError(f"Unknown production type: {prod_type}")

        # -- Get the columns to select
        if agg == "sum":
            agg_func = func.sum
        elif agg == "mean":
            agg_func = func.avg
        elif agg == "count":
            agg_func = func.count
        elif agg == "max":
            agg_func = func.max
        elif agg == "min":
            agg_func = func.min
        else:
            raise ValueError(f"Unknown aggregation function: {agg}")

        s_cols = [
            table.c[self.P_DATE],
            agg_func(table.c[self.P_WELLS]).label(self.P_WELLS),
            agg_func(table.c[self.P_PRODUCTION]).label(self.P_PRODUCTION),
        ]

        if lease_ids is not None:
            s = (
                select(s_cols)
                .where(table.c[self.P_LEASE_ID].in_(lease_ids))
                .group_by(table.c[self.P_DATE])
            )
        else:
            s = select(s_cols).group_by(table.c[self.P_DATE])

        df = pd.read_sql(s, self.engine)

        if get_rate:
            # Parse date column and set as index and order it
            df[self.P_DATE] = pd.to_datetime(df[self.P_DATE])
            # Calculate the number of days in each month
            df["N_DAYS"] = df[self.P_DATE].dt.daysinmonth
            # Calculate the calendar day production
            df[self.CV_P_CAL_DAY_PROD] = df[self.P_PRODUCTION] / df["N_DAYS"]
            df = df.drop(columns=["N_DAYS"])

        df = df.set_index(self.P_DATE).sort_index()
        return df
