import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def __calculate_income(series: pd.Series):
    # Define entry point
    prices = series.iloc[:, 1]
    entry_point = series[prices == prices.min()]

    # Find region where we can sell stock
    sell_region = series[series.index > entry_point.index[0]]

    # Define exit point
    prices = sell_region.iloc[:, 1]
    exit_point = sell_region[prices == prices.max()]

    # Calculate income
    income = round(exit_point.values[0][1] - entry_point.values[0][1], 2)
    return income


def PMM(predicted: pd.Series, real: pd.Series) -> dict:
    """
    Profit-Money-Metric
    Calculates the metric of prediction and
    real data in order to investigate prediction
    in money profit purpose
    All arguments must be of equal length.
    :param predicted: predicted data
    :param real: real data
    :return: data investigation result
    """

    # Supposed income calculation
    supposed_income = __calculate_income(predicted)

    # Real income calculation
    real_income = __calculate_income(real)

    # Difference between incomes calculation
    diff = real_income - supposed_income

    # Trend designation
    if diff > 0:
        trend = 'positive'
    elif diff < 0:
        trend = 'negative'
    else:
        trend = 'exact'

    # TODO calculate quantity of predicted patterns

    return {'supposed income': supposed_income,
            'real_income': real_income,
            'diff': abs(diff),
            'trend': trend}