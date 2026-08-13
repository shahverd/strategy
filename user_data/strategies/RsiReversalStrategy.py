from pandas import DataFrame
import talib.abstract as ta

from freqtrade.strategy import IStrategy


class RsiReversalStrategy(IStrategy):
    INTERFACE_VERSION = 3
    can_short = False
    timeframe = "1h"
    startup_candle_count = 30
    stoploss = -0.10
    minimal_roi = {"0": 0.04, "240": 0.01, "480": 0.0}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        recovered_from_oversold = (dataframe["rsi"] > 30) & (dataframe["rsi"].shift(1) <= 30)
        dataframe.loc[recovered_from_oversold & (dataframe["volume"] > 0), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(dataframe["rsi"] >= 70) & (dataframe["volume"] > 0), "exit_long"] = 1
        return dataframe
