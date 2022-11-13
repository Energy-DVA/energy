from sqlalchemy import create_engine, MetaData, or_, and_
from sqlalchemy import select, func
from _1_analysis.db_schema import (
    OIL_PROD_TABLE,
    GAS_PROD_TABLE,
    LEASE_TABLE,
    WELLS_TABLE,
    TOPS_TABLE,
)
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima
from pmdarima import model_selection

#%%
class CFG:
    img_dim1 = 16
    img_dim2 = 12


plt.rcParams.update({"figure.figsize": (CFG.img_dim1, CFG.img_dim2)})


engine = create_engine("sqlite:///data/kansas_oil_gas.db")
# Reflect oil production table
meta = MetaData()
meta.reflect(bind=engine)
oil_prod = meta.tables[OIL_PROD_TABLE]
gas_prod = meta.tables[GAS_PROD_TABLE]
lease = meta.tables[LEASE_TABLE]
wells = meta.tables[WELLS_TABLE]
tops = meta.tables[TOPS_TABLE]


s = select(
    [
        gas_prod.c.DATE,
        func.sum(gas_prod.c.WELLS).label("N_WELLS"),
        func.sum(gas_prod.c.PRODUCTION).label("MONTHLY_GAS_PROD"),
    ]
).group_by(gas_prod.c.DATE)
df_gas_prod = pd.read_sql(s, engine)


df_gas_prod["DATE"] = pd.to_datetime(df_gas_prod["DATE"])
df_gas_prod.set_index("DATE", inplace=True)
df_gas_prod.head()

# Train & Test Split
test_obs = 36

xtrain, xvalid = model_selection.train_test_split(df_gas_prod, test_size=test_obs)
print(xtrain.shape, xvalid.shape)
#%%
# SARIMA (Seasonal ARIMA)
model_sarima = auto_arima(
    xtrain["MONTHLY_GAS_PROD"],
    start_p=0,
    d=1,
    start_q=0,
    start_P=0,
    D=1,
    start_Q=0,
    m=12,
    seasonal=True,
    test="adf",
    stepwise=True,
    trace=True,
    error_action="ignore",
    suppress_warnings=True,
)

fitted, confint = model_sarima.predict(
    xvalid["MONTHLY_GAS_PROD"].shape[0], return_conf_int=True, alpha=0.05
)
lower_conf = pd.Series(confint[:, 0], index=xvalid.index)
upper_conf = pd.Series(confint[:, 1], index=xvalid.index)

plt.plot(df_gas_prod["MONTHLY_GAS_PROD"], color="black", label="MONTHLY_GAS_PROD")
plt.plot(pd.Series(fitted), color="red", label="SARIMA Prediction")
# plt.plot(hw_pred, color='green', label='Holt-Winters smoothing prediction')
plt.plot(lower_conf, color="blue", label="SARIMA 95% Lower Confidence Level")
plt.plot(upper_conf, color="blue", label="SARIMA 95% Upper Confidence Level")
plt.fill_between(lower_conf.index, lower_conf, upper_conf, color="k", alpha=0.15)
plt.title("Overall Gas production prediction")
plt.legend(loc="lower left", fontsize=12)
plt.show()


#%%
# SARIMAX (Seasonal ARIMA with Exogeneous Time Series)

model_sarimax = auto_arima(
    xtrain["MONTHLY_GAS_PROD"],
    X=xtrain[["N_WELLS"]],
    start_p=0,
    d=1,
    start_q=0,
    start_P=0,
    D=1,
    start_Q=0,
    m=12,
    seasonal=True,
    test="adf",
    stepwise=True,
    trace=True,
    error_action="ignore",
    suppress_warnings=True,
)

fittedx, confintx = model_sarimax.predict(
    xvalid["MONTHLY_GAS_PROD"].shape[0],
    X=xvalid[["N_WELLS"]],
    return_conf_int=True,
    alpha=0.05,
)
lower_confx = pd.Series(confintx[:, 0], index=xvalid.index)
upper_confx = pd.Series(confintx[:, 1], index=xvalid.index)

plt.plot(df_gas_prod["MONTHLY_GAS_PROD"], color="black", label="MONTHLY_GAS_PROD")

plt.plot(pd.Series(fittedx), color="red", label="SARIMAX Prediction")
plt.plot(lower_confx, color="lightcoral", label="SARIMAX 95% Lower Confidence Level")
plt.plot(upper_confx, color="lightcoral", label="SARIMAX 95% Upper Confidence Level")

plt.fill_between(lower_conf.index, lower_confx, upper_confx, color="k", alpha=0.15)
plt.title("Overall Gas production prediction")
plt.legend(loc="lower left", fontsize=12)
plt.show()
