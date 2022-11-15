from pmdarima.arima import auto_arima
import pandas as pd
from typing import Optional, Union, List


class Forecaster:
    START_P = 0
    START_Q = 0
    FIRST_DIFF = 1
    SEAS_START_P = 0
    SEAS_START_Q = 0
    SEAS_FIRST_DIFF = 1
    PERIODS_SEASON = 12
    TEST = "adf"
    SEASONAL = True
    STEPWISE = True
    ERROR_ACTION = "ignore"
    SUPPRESS_WARNINGS = True
    ALPHA = 0.05
    # Result columns
    RES_FORECAST = "forecast"
    RES_X_VAR = "x_var"
    RES_LOWER_INTERVAL = "lower_interval"
    RES_UPPER_INTERVAL = "upper_interval"

    def __init__(
        self,
        y: pd.Series,
        X: Optional[Union[pd.Series, pd.DataFrame, list]] = None,
    ):
        """
        Constructor for Forecaster class.

        Parameters
        ----------
        y
            The time series to forecast. It must be a pandas Series with a
            DatetimeIndex.
        X
            The exogenous variables to use in the forecast. It can be a pandas Series
            or a pandas DataFrame with a DatetimeIndex.
        """

        self.y = y
        self.X = X
        self.n_periods = None
        self._model = None

    @property
    def model(self):
        if self._model is None:
            return ValueError("The model has not been fitted yet.")

        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def fit(self):
        self.model = auto_arima(
            self.y,
            X=self.X,
            start_p=self.START_P,
            d=self.FIRST_DIFF,
            start_q=self.START_Q,
            start_P=self.SEAS_START_P,
            D=self.SEAS_FIRST_DIFF,
            start_Q=self.SEAS_START_Q,
            m=self.PERIODS_SEASON,
            seasonal=self.SEASONAL,
            test=self.TEST,
            stepwise=self.STEPWISE,
            error_action=self.ERROR_ACTION,
            suppress_warnings=self.SUPPRESS_WARNINGS,
        )

    def predict(self, n_periods: int, X: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        self.n_periods = n_periods

        if self.X is not None and X is None:
            raise ValueError(
                "The exogenous variables must be provided to make the forecast."
            )

        x_var = X.copy() if X is not None else None
        forecast, confint = self.model.predict(
            n_periods=n_periods, X=x_var, return_conf_int=True, alpha=self.ALPHA
        )
        # Create a DataFrame with the results
        df_forecast = pd.DataFrame(
            {
                self.RES_FORECAST: forecast.values,
                self.RES_LOWER_INTERVAL: confint[:, 0],
                self.RES_UPPER_INTERVAL: confint[:, 1],
            },
            index=forecast.index,
        )

        if x_var is not None:
            x_var.index = forecast.index
            # Rename x_var columns
            x_var.rename(
                columns={col: self.RES_X_VAR + "_" + str(col) for col in x_var.columns},
                inplace=True,
            )
            # Concat x_var in results data frame
            df_forecast = pd.concat([df_forecast, x_var], axis=1)

        return df_forecast

    def fit_predict(
        self, n_periods: int, x_var: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        self.fit()
        return self.predict(n_periods, x_var)
