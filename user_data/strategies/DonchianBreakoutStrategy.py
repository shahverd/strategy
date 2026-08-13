from freqtrade.strategy import IStrategy
from pandas import DataFrame


class DonchianBreakoutStrategy(IStrategy):
    INTERFACE_VERSION = 3
    can_short = True
    timeframe = "4h"
    startup_candle_count = 30
    stoploss = -0.12
    minimal_roi = {"0": 0.10, "720": 0.03, "1440": 0.0}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["upper_channel"] = dataframe["high"].rolling(20).max().shift(1)
        dataframe["lower_channel"] = dataframe["low"].rolling(20).min().shift(1)
        dataframe["exit_upper"] = dataframe["high"].rolling(10).max().shift(1)
        dataframe["exit_lower"] = dataframe["low"].rolling(10).min().shift(1)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["close"] > dataframe["upper_channel"]) & (dataframe["volume"] > 0),
            "enter_long",
        ] = 1
        dataframe.loc[
            (dataframe["close"] < dataframe["lower_channel"]) & (dataframe["volume"] > 0),
            "enter_short",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["close"] < dataframe["exit_lower"], "exit_long"] = 1
        dataframe.loc[dataframe["close"] > dataframe["exit_upper"], "exit_short"] = 1
        return dataframe
