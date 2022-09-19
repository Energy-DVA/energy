import pandas as pd
from prodphecy import normalize_date_freq


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


def convert_month_year(row, date_col="DATE", prod_col="PRODUCTION"):
    x = pd.DataFrame(row).T
    dates = pd.date_range(start=x[date_col].iloc[0], periods=12, freq="MS")
    x[prod_col] = x[prod_col] / 12
    x.set_index(date_col, inplace=True)
    x = x.reindex(dates, method="ffill")
    return x.reset_index().to_numpy()


def preprocess_prod(df_prod, id_col, date_col, wells_col, prod_col):
    # --- Start processing the yearly production data ---
    # Select dates starting with 0
    yearly_dates = df_prod[date_col].str.startswith("0")
    df_year = df_prod[yearly_dates]
    if len(df_year) > 0:
        df_year = df_year.assign(**{date_col: df_year[date_col].str.replace("0", "1", 1)})
        df_year = (
            df_year.assign(**{date_col: pd.to_datetime(df_year[date_col])})
            .apply(convert_month_year, axis=1, args=(date_col, prod_col))
            .explode()
        )
        df_year = pd.DataFrame(df_year.to_list(), columns=df_prod.columns)

    # --- Process the monthly production data ---
    df = df_prod[~yearly_dates]
    df = df.assign(**{date_col: pd.to_datetime(df[date_col])})
    df = (
        df.set_index(date_col)
        .groupby(id_col)
        .apply(
            lambda g: normalize_date_freq(
                g,
                "MS",
                cols_fill_na=[wells_col, prod_col],
                fill_na=0.0,
                method_no_cols="ffill",
            )
        )
        .reset_index(0, drop=True)
        .reset_index()
    )
    df = pd.concat([df, df_year])
    return df


def read_prod_data(data_path):
    df = (
        pd.read_csv(
            data_path,
            compression="zip",
            header=0,
        )
        .rename({"MONTH-YEAR": "DATE"}, axis=1)
        .drop(DROP_PROD_COLS, axis=1)
    )
    return preprocess_prod(df, "LEASE_KID", "DATE", "WELLS", "PRODUCTION")
