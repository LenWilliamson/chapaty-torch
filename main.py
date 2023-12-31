import sys
from typing import Optional
import df_schema as schema
import pandas as pd
from functools import partial
from util.converter import posix_to_homan_readable_timestamp
import plotly.graph_objects as go

def csv_to_df(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def plot_ohlc(path: str) -> None:
    df_ohlc = csv_to_df(path)
     # Transform open timestamp from milliseconds to human readable datetime format "%Y-%m-%d %H-%M-%S"
    df_ohlc[schema.OHLC_CN['openTime']] = df_ohlc[schema.OHLC_CN['openTime']].map(
        partial(posix_to_homan_readable_timestamp))
    fig_ohlc = go.Figure(
        data=[
            go.Candlestick(
                x=df_ohlc[schema.OHLC_CN['openTime']],
                open=df_ohlc[schema.OHLC_CN['open']],
                high=df_ohlc[schema.OHLC_CN['high']],
                low=df_ohlc[schema.OHLC_CN['low']],
                close=df_ohlc[schema.OHLC_CN['close']],
                xaxis='x',
                yaxis='y',
                showlegend=False
            )
        ],
        layout=go.Layout(
            title=go.layout.Title(
                text='6e 2022')
        )
    )
    fig_ohlc.show()

def round_price_histogram_by(df: pd.DataFrame, factor: int) -> pd.DataFrame:
    df['px'] = (df['px'] / factor).round() * factor
    return df.groupby('px')['qx'].max().reset_index()

def plot_price_histogram_vertically(path: str, round_factor: Optional[int]) -> None:
    df_vol = csv_to_df(path)
    if round_factor:
        df_vol = round_price_histogram_by(df_vol, round_factor)
    fig_volume = go.Figure(
        data=[
            go.Bar(
                base=0,
                x=df_vol[schema.VOLP_CN['price']],
                y=df_vol[schema.VOLP_CN['quantity']],
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
    fig_volume.show()

def plot_price_histogram_horizontally(path: str, round_factor: Optional[int]) -> None:
    df_vol = csv_to_df(path)
    if round_factor:
        df_vol = round_price_histogram_by(df_vol, round_factor)
    fig_volume_h = go.Figure(
        data=[
            go.Bar(
                base=0,
                x=df_vol[schema.VOLP_CN['quantity']],
                y=df_vol[schema.VOLP_CN['price']],
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
    fig_volume_h.show()


def plot_ohlc_with_price_histogram_horizontally(ohlc_path: str, price_histogram_path: str, round_factor: Optional[int]) -> None:
    df_ohlc = csv_to_df(ohlc_path)
    df_ohlc[schema.OHLC_CN['openTime']] = df_ohlc[schema.OHLC_CN['openTime']].map(
        partial(posix_to_homan_readable_timestamp))
    df_vol = csv_to_df(price_histogram_path)
    if round_factor:
        df_vol = round_price_histogram_by(df_vol, round_factor)
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df_ohlc[schema.OHLC_CN['openTime']],
                open=df_ohlc[schema.OHLC_CN['open']],
                high=df_ohlc[schema.OHLC_CN['high']],
                low=df_ohlc[schema.OHLC_CN['low']],
                close=df_ohlc[schema.OHLC_CN['close']],
                xaxis='x',
                yaxis='y',
                showlegend=False
            ),
            go.Bar(
                base=0,
                x=df_vol[schema.VOLP_CN['quantity']],
                y=df_vol[schema.VOLP_CN['price']],
                orientation='h',
                xaxis='x2',
                yaxis='y2',
                showlegend=False,
                marker=go.bar.Marker(color='#000')
            )
        ],
        layout=go.Layout(
            title=go.layout.Title(
                text='OHLC with Price Histogram'),
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
    fig.show()


def main() -> int:
    cme_ohlc_path = 'gs://chapaty-ai-hdb-test/cme/ohlc/ohlc_data_for_tpo_test.csv'
    cme_price_histogram_path = 'gs://chapaty-ai-test/ppp/_test_data_files/target_ohlc_tpo_for_tpo_test.csv'
    binance_ohlc_path = 'gs://chapaty-ai-hdb-test/binance/ohlcv/ohlc_data_for_tpo_test.csv'
    binance_price_histogram_path = 'gs://chapaty-ai-test/ppp/btcusdt/2022/Mon1h0m-Fri23h0m/1d/target_binance_tpo_from_ohlc.csv'
    ohlc_path = binance_ohlc_path
    price_histogram_path = binance_price_histogram_path
    round_factor = 8

    plot_ohlc(ohlc_path)
    plot_price_histogram_vertically(price_histogram_path, round_factor)
    plot_price_histogram_horizontally(price_histogram_path, round_factor)
    plot_ohlc_with_price_histogram_horizontally(ohlc_path, price_histogram_path, round_factor)
    return 0


if __name__ == '__main__':
    sys.exit(main())
