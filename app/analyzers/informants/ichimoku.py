""" Ichimoku Indicator
"""

import math

import numpy
import pandas
from talib import abstract

from analyzers.utils import IndicatorUtils


class Ichimoku(IndicatorUtils):
    def analyze(self, historical_data):
        """Performs an ichimoku cloud analysis on the historical data

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.

        Returns:
            dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
                indication.
        """

        tenkansen_period = 9
        kijunsen_period = 26
        leading_span_b_period = 52

        dataframe = self.convert_to_dataframe(historical_data)

        ichimoku_columns = {
            'tenkansen': [numpy.nan] * dataframe.index.shape[0],
            'kijunsen': [numpy.nan] * dataframe.index.shape[0],
            'leading_span_a': [numpy.nan] * dataframe.index.shape[0],
            'leading_span_b': [numpy.nan] * dataframe.index.shape[0]
        }

        ichimoku_values = pandas.DataFrame(
            ichimoku_columns,
            index=dataframe.index
        )

        ichimoku_df_size = ichimoku_values.shape[0]

        for index in range(tenkansen_period, ichimoku_df_size):
            start_index = index - tenkansen_period
            last_index = index + 1
            tankansen_min = dataframe['low'][start_index:last_index].min()
            tankansen_max = dataframe['high'][start_index:last_index].max()
            ichimoku_values['tenkansen'][last_index-1] = (tankansen_min + tankansen_max) / 2

        for index in range(kijunsen_period, ichimoku_df_size):
            start_index = index - kijunsen_period
            last_index = index + 1
            kijunsen_min = dataframe['low'][start_index:last_index].min()
            kijunsen_max = dataframe['high'][start_index:last_index].max()
            ichimoku_values['kijunsen'][last_index-1] = (kijunsen_min + kijunsen_max) / 2

        for index in range(leading_span_b_period, ichimoku_df_size):
            start_index = index - leading_span_b_period
            last_index = index + 1
            leading_span_b_min = dataframe['low'][start_index:last_index].min()
            leading_span_b_max = dataframe['high'][start_index:last_index].max()
            ichimoku_values['leading_span_b'][last_index-1] = (
                leading_span_b_min + leading_span_b_max
            ) / 2

        ichimoku_values['leading_span_a'] = (
            ichimoku_values['tenkansen'] + ichimoku_values['kijunsen']
        ) / 2

        ichimoku_values.dropna(how='any', inplace=True)

        return ichimoku_values
