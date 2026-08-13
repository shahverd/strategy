import talib.abstract as ta
from freqtrade.strategy import IStrategy
from pandas import DataFrame


class EmaCrossStrategy(IStrategy):
    INTERFACE_VERSION = 3
    can_short = True
    timeframe = "1h"
    startup_candle_count = 50
    stoploss = -0.08
    minimal_roi = {"0": 0.06, "180": 0.02, "360": 0.0}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema_fast"] = ta.EMA(dataframe, timeperiod=12)
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=26)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        crossed_up = (dataframe["ema_fast"] > dataframe["ema_slow"]) & (
            dataframe["ema_fast"].shift(1) <= dataframe["ema_slow"].shift(1)
        )
        crossed_down = (dataframe["ema_fast"] < dataframe["ema_slow"]) & (
            dataframe["ema_fast"].shift(1) >= dataframe["ema_slow"].shift(1)
        )
        dataframe.loc[crossed_up & (dataframe["volume"] > 0), "enter_long"] = 1
        dataframe.loc[crossed_down & (dataframe["volume"] > 0), "enter_short"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["ema_fast"] < dataframe["ema_slow"], "exit_long"] = 1
        dataframe.loc[dataframe["ema_fast"] > dataframe["ema_slow"], "exit_short"] = 1
        return dataframe
