# import numpy as np
# import scipy.optimize
import datetime as dt
from typing import Tuple
import itertools


# def optimize_hyperparams(backtest_obj: object, backtest_params: dict, days: int) -> Tuple[float, float]:
#     def minus_pnl_function(params: list) -> float:
#         backtest_params['delta_hedge_significance'] = params[0]
#         backtest_params['vol_diff_significance'] = params[1]
#         print(params[0], params[1])
#         return -sum(backtest_obj(**backtest_params).backtest(days_strategy=days))
#
#     hyperparams = np.array([0.001, 0.001])
#
#     # Find solution via minimization of "minus PnL" function by hyperparams optimization
#     solution = scipy.optimize.minimize(minus_pnl_function, hyperparams, bounds=[(0.0, 1), (0.0, 0.1)])
#
#     return solution

def optimize_hyperparams(backtest_obj, backtest_params: dict, days: int) -> Tuple[float, float]:
    change = 1
    bounds_percentage = [(0, 100), (0, 10)]

    iterables = [list(range(b[0], b[1], change)) for b in bounds_percentage]

    solution = (0, 0)
    pnl_prev = 0
    for d in iterables[0]:
        for v in iterables[1]:
            d /= 100
            v /= 100
            backtest_params['delta_hedge_significance'] = d
            backtest_params['vol_diff_significance'] = v
            pnl = sum(backtest_obj(**backtest_params).backtest(days_strategy=days))
            if pnl > pnl_prev:
                pnl_prev = pnl
                solution = (d, v)

            print(pnl)
            print((d, v))

    return solution


if __name__ == '__main__':
    from backtester_hyperparams import BacktesterOffshoreLocalRealized

    fx_pair = 'EURUSD'
    days_strat = 5
    start_test = dt.datetime(year=2022, month=4, day=1)
    end_test = dt.datetime(year=2022, month=10, day=1)

    backtest = {'asset': fx_pair, 'rf_base_ccy': 0.004, 'rf_second_ccy': 0.025, 'datetime_start': start_test,
                'datetime_end': end_test, 'onshore_spread': 0.002, 'offshore_spread': 0.0005}

    optimal_hyperparams = optimize_hyperparams(BacktesterOffshoreLocalRealized, backtest, days=days_strat)

    print(optimal_hyperparams)
