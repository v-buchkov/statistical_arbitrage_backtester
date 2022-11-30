from backtester_hyperparams import BacktesterOffshoreLocalRealized
import datetime as dt
import numpy as np
from stat_arb.src.plt.graphs import plot_barchart, plot_line_chart

if __name__ == '__main__':
    """ HYPERPARAMETERS """
    # Percentage (in decimal) difference between volume to hedge open delta to zero versus transaction cost
    # Compared as delta_hedge_cost * (1 + DELTA_SIGNIFICANCE) vs transaction cost
    DELTA_SIGNIFICANCE = 0.2
    # Difference between volatilities that assume to be significant
    # Compared as vol_one - vol_two vs VOL_SIGNIFICANCE
    VOL_SIGNIFICANCE = 0.05

    fx_pair = 'EURUSD'
    days_strat = [5, 10, 20, 30]
    start_test = dt.datetime(year=2022, month=4, day=1)
    end_test = dt.datetime(year=2022, month=10, day=1)

    for days in days_strat:
        # Object is recreated to reinitialize all stored data (arrays)
        backtest = BacktesterOffshoreLocalRealized(delta_hedge_significance=DELTA_SIGNIFICANCE,
                                                   vol_diff_significance=VOL_SIGNIFICANCE, asset=fx_pair,
                                                   rf_base_ccy=0.004, rf_second_ccy=0.025,
                                                   datetime_start=start_test, datetime_end=end_test,
                                                   onshore_spread=0.002, offshore_spread=0.0005)

        print(f'{days} days:')
        print('---')

        backtest_results = backtest.backtest(days_strategy=days)

        print(f'Hist vols: {backtest.hist_vols}')

        strat = backtest_results
        cumulative_strat = [sum(strat[:i]) for i in range(2, len(strat))]

        strat_trades = [p for p in strat if p != 0]
        strat_mean = np.mean(strat_trades)
        strat_std = np.std(strat_trades)

        print('Strategy:')
        pnl_distr = ['{:+,.2f}'.format(p) for p in strat]
        print(f'PnL distribution: {pnl_distr}')
        print('Total PnL = {:+,.2f}'.format(sum(strat)))
        print('Average per trade = {:+,.2f}'.format(strat_mean))
        print('t-value = {:.2f}\n'.format(strat_mean / strat_std * np.sqrt(len(strat_trades))))

        plot_barchart(dates=backtest.backtesting_date, data=strat, name=f'{fx_pair} PnL {days} days')
        plot_line_chart(dates=backtest.backtesting_date[2:], data=cumulative_strat,
                        name=f'{fx_pair} Cumulative PnL {days} days', label='Cumulative PnL')
