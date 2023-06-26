import sys
import os
import data_config as dc
import pandas as pd
from functools import partial
from util.tools import time_converter
import plotly.graph_objects as go


def plot(volume_prev_cw: str, ohlc_prev_cw: str, ohlc_current_cw) -> None:
    """
    This function plots the OHLC data together with the selected volume profile. We always plot the OHLC data of two consecutive weeks.
    Note, the input of "volume_prev_cw" and "ohlc_prev_cw" should be identical. We evaluate the strategy in the "current" week.
    :param volume_prev_cw: calendar week of the volume profile
    :param ohlc_prev_cw: calendar week of OHLC data in the previous week
    :param ohlc_current_cw: calendar week of OHLC data in the current week 
    """

    # Set file paths
    file_path_volume_prev_cw: str = os.path.join(dc.VOLP_DP, volume_prev_cw)
    file_path_ohlc_prev_cw: str = os.path.join(dc.OHLC_DP, ohlc_prev_cw)
    file_path_ohlc_current_cw: str = os.path.join(dc.OHLC_DP, ohlc_current_cw)

    # Load OHLC data into two separate DataFrames
    df_ohlc_prev: pd.DataFrame = pd.read_csv(
        file_path_ohlc_prev_cw, sep=',', names=dc.OHLC_CNL, header=0)
    df_ohlc_current: pd.DataFrame = pd.read_csv(
        file_path_ohlc_current_cw, sep=',', names=dc.OHLC_CNL, header=0)

    # Join OHLC data into single DataFrame
    df_ohlc: pd.DataFrame = pd.concat(
        [df_ohlc_prev, df_ohlc_current], axis=0, ignore_index=True)

    # df_ohlc = df_ohlc_current

    # Load Volume profile into DataFrame
    df_vol: pd.DataFrame = pd.read_csv(
        file_path_volume_prev_cw, sep=',', names=dc.VOL_CNL, header=0)

    # Transform open timestamp from milliseconds to human readable datetime format "%Y-%m-%d %H-%M-%S"
    df_ohlc[dc.OHLC_CN['openTime']] = df_ohlc[dc.OHLC_CN['openTime']].map(
        partial(time_converter))

    # Generate plot: OHLC with volume profile
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df_ohlc[dc.OHLC_CN['openTime']],
                open=df_ohlc[dc.OHLC_CN['open']],
                high=df_ohlc[dc.OHLC_CN['high']],
                low=df_ohlc[dc.OHLC_CN['low']],
                close=df_ohlc[dc.OHLC_CN['close']],
                xaxis='x',
                yaxis='y',
                showlegend=False
            ),
            go.Bar(
                base=0,
                x=df_vol[dc.VOLP_CN['quantity']],
                y=df_vol[dc.VOLP_CN['price']],
                orientation='h',
                xaxis='x2',
                yaxis='y2',
                showlegend=False,
                marker=go.bar.Marker(color='#000')
            )
        ],
        layout=go.Layout(
            title=go.layout.Title(
                text=f'BTC-USDT OHLC with volume in calendar week: vol={volume_prev_cw} and ohlc=[{ohlc_prev_cw} | {ohlc_current_cw}]'),
            xaxis=go.layout.XAxis(
                side='bottom',
                title='Date',
                showticklabels=True,
                overlaying='x2'
            ),
            yaxis=go.layout.YAxis(
                side='left',
                title='Price',
                showticklabels=True,
                overlaying='y2'
            ),
            xaxis2=go.layout.XAxis(
                side='top',
                title='Volume',
                rangeslider=go.layout.xaxis.Rangeslider(visible=False),
                showticklabels=True
            ),
            yaxis2=go.layout.YAxis(
                showticklabels=False,
                side='right',
                matches='y'
            )
        )
    )

    # Generate plot: OHLC
    fig_ohlc = go.Figure(
        data=[
            go.Candlestick(
                x=df_ohlc[dc.OHLC_CN['openTime']],
                open=df_ohlc[dc.OHLC_CN['open']],
                high=df_ohlc[dc.OHLC_CN['high']],
                low=df_ohlc[dc.OHLC_CN['low']],
                close=df_ohlc[dc.OHLC_CN['close']],
                xaxis='x',
                yaxis='y',
                showlegend=False
            )
        ],
        layout=go.Layout(
            title=go.layout.Title(
                text=f'BTC-USDT OHLC file in calendar week [{ohlc_prev_cw} | {ohlc_current_cw}]')
        )
    )

    fig_volume = go.Figure(
        data=[
            go.Bar(
                base=0,
                x=df_vol[dc.VOLP_CN['price']],
                y=df_vol[dc.VOLP_CN['quantity']],
                orientation='v',
                xaxis='x',
                yaxis='y',
                showlegend=False,
                marker=go.bar.Marker(color='#000')
            )
        ],
        layout=go.Layout(
            title=go.layout.Title(text='y = Volume'),
            xaxis=go.layout.XAxis(
                side='bottom',
                title='Price',
                showticklabels=True,
            ),
            yaxis=go.layout.YAxis(
                side='left',
                title='Volume',
                showticklabels=True,
            ),
        )
    )

    fig_volume_h = go.Figure(
        data=[
            go.Bar(
                base=0,
                x=df_vol[dc.VOLP_CN['quantity']],
                y=df_vol[dc.VOLP_CN['price']],
                orientation='h',
                xaxis='x',
                yaxis='y',
                showlegend=False,
                marker=go.bar.Marker(color='#ff0000')
            )
        ],
        layout=go.Layout(
            title=go.layout.Title(text='Volume'),
            xaxis=go.layout.XAxis(
                side='bottom',
                title='Volume',
                showticklabels=True,
            ),
            yaxis=go.layout.YAxis(
                side='left',
                title='Price',
                showticklabels=True,
            ),
        )
    )

    fig.show()
    fig_ohlc.show()
    fig_volume.show()
    fig_volume_h.show()


def main() -> int:
    # BEGIN: To configure the plot change the following lines
    # NOTE: Winter time => UTC+1 (end of October to end of March) | Summer time => UTC+2 | https://currentmillis.com/
    calendar_week: int = 11
    day: int = 5
    # END: To configure the plot change the following lines

    # 11_3 ist interessant

    volume_prev_cw: str = f'{calendar_week}_{day - 1}.csv'
    ohlc_prev_cw: str = f'{calendar_week}_{day - 1}.csv'
    ohlc_current_cw: str = f'{calendar_week}_{day}.csv'

    plot(volume_prev_cw=volume_prev_cw, ohlc_prev_cw=ohlc_prev_cw,
         ohlc_current_cw=ohlc_current_cw)
    return 0


if __name__ == '__main__':
    sys.exit(main())
