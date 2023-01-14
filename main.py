import datetime as dt

from contextlib import redirect_stdout

from stat_arb.src.plt.graphs import plot_barchart, plot_line_chart
from backtester import FixedLevelStrategy, DynamicDeltaHedgeStrategy

if __name__ == '__main__':

    fx_pair = 'EURUSD'
    days_strat = [5, 10, 20, 30]
    start_test = dt.datetime(year=2022, month=4, day=1)
    end_test = dt.datetime(year=2022, month=10, day=1)
    fixed_vol = False

    if fixed_vol:
        file_name = f'output/Backtest_{fx_pair}_FixedVol.txt'
    else:
        file_name = f'output/Backtest_{fx_pair}.txt'

    backtest = DynamicDeltaHedgeStrategy(asset=fx_pair, rf_base_ccy=0.004, rf_second_ccy=0.025,
                                         datetime_start=start_test, datetime_end=end_test,
                                         onshore_spread=0.002, offshore_spread=0.0005)

    # with open(file_name, 'w') as out_f:
    #     with redirect_stdout(out_f):
    for days in days_strat:

        backtest.backtest(days_strategy=days, use_fixed_vol=fixed_vol)

        print(f'{days} days:')
        print('---')

        print(f'Hist vols: {backtest.hist_vols}')

        print('Strategy:')
        pnl_distr = ['{:+,.2f}'.format(p) for p in backtest.pnl_distribution_by_trades]
        print(f'PnL distribution: {pnl_distr}')
        print('Total PnL = {:+,.2f}'.format(backtest.pnl_total))
        print('Average per trade = {:+,.2f}'.format(backtest.pnl_mean))
        print('t-statistic = {:.2f}\n'.format(backtest.t_statistic))
        print('p-value = {:.2f}\n'.format(backtest.t_test_p_value))

        if fixed_vol:
            barchart_name = f'{fx_pair} PnL {days} days (Fixed Vol)'
            cumulative_name = f'{fx_pair} Cumulative PnL {days} days (Fixed Vol)'
        else:
            barchart_name = f'{fx_pair} PnL {days} days'
            cumulative_name = f'{fx_pair} Cumulative PnL {days} days'

        plot_barchart(dates=backtest.backtesting_dates, data=backtest.backtest_path,
                      name=barchart_name)
        plot_line_chart(dates=backtest.backtesting_dates[2:], data=backtest.pnl_distribution_cumulative,
                        name=cumulative_name, label='Cumulative PnL')
